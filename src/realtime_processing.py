import cv2
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient
from collections import defaultdict
from api_client import APIClient
from database import DatabaseManager

# --- PARÂMETROS DE CONFIGURAÇÃO ---
VIDEO_SOURCE = 0  # Use 0 para webcam (para escanear em tempo real) ou o caminho para um arquivo de vídeo

# Modelo local para RASTREAMENTO (tracking)
TRACKING_MODEL_PATH = 'yolov8n.pt'
TRACKING_CLASS_ID = [3]  # Classe 'motorcycle' no modelo COCO

# --- CONFIGURAÇÃO ROBOFLOW HTTP API (para CLASSIFICAÇÃO) ---
ROBOFLOW_API_URL = "https://detect.roboflow.com"
ROBOFLOW_API_KEY = "aFBnNsh545I9GTlTUzpa"
ROBOFLOW_MODEL_ID = "mottu-iot-iycbr/1"

CONFIDENCE_THRESHOLD = 0.5  # Limiar de confiança para o RASTREAMENTO (tracking)
CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.80  # 80% de confiança para a CLASSIFICAÇÃO do modelo
FRAMES_PARA_CONFIRMAR_SAIDA = 15  # Nº de frames que uma moto deve estar ausente para ser considerada como 'saiu'

# --- URL DA API ---
API_BASE_URL = "https://gef-mottu-dev-app-a2dffngahzayd3an.brazilsouth-01.azurewebsites.net/api"

def format_model_name(name_from_api):
    if name_from_api == 'mottu_e':
        return 'Mottu-E'
    elif name_from_api == 'mottu_pop':
        return 'Mottu Pop'
    elif name_from_api == 'mottu_sport':
        return 'Mottu Sport'
    else:
        return name_from_api.replace('_', ' ').title()
    

def processa_frame(frame, tracking_model, roboflow_client, db_manager, api_client):
    # 1. Rastreia objetos da classe 'motorcycle' para obter IDs estáveis
    results = tracking_model.track(frame, persist=True, classes=TRACKING_CLASS_ID, conf=CONFIDENCE_THRESHOLD)

    motos_no_frame_atual = set()
    annotated_frame = frame.copy()

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)

        for i, (box, track_id) in enumerate(zip(boxes, track_ids)):
            moto_id_str = f'moto_{track_id}'
            motos_no_frame_atual.add(moto_id_str)

            # 2. Recorta a imagem da moto e envia para o Roboflow para classificar o modelo
            x1, y1, x2, y2 = box
            cropped_moto = frame[y1:y2, x1:x2]
            classification_result = roboflow_client.infer(cropped_moto, model_id=ROBOFLOW_MODEL_ID)

            # A API retorna um dicionário. Acessamos as predições e o nome da classe usando chaves.
            predictions = classification_result.get('predictions', [])
            model_name = 'Analisando...'  # Valor padrão para exibição
            
            if predictions:
                top_prediction = predictions[0]
                confidence = top_prediction.get('confidence', 0)

                # CONDIÇÃO PRINCIPAL: Só registra no banco e envia para a API se a confiança for alta
                if confidence >= CLASSIFICATION_CONFIDENCE_THRESHOLD:
                    raw_model_name = top_prediction['class']
                    model_name = format_model_name(raw_model_name)
                    
                    # Calcula o centro da moto para registrar sua localização
                    center_x = (box[0] + box[2]) // 2
                    center_y = (box[1] + box[3]) // 2

                    db_manager.insert_detection(moto_id_str, int(center_x), int(center_y), model_name)
                    api_client.send_detection_event(moto_id_str, model_name, int(center_x), int(center_y), status="em_patio")
                else:
                    model_name = 'Modelo Incerto'  # Se a confiança for baixa, apenas exibe na tela

            # Desenha anotações no frame
            label = f"ID: {track_id} - {model_name}"
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return annotated_frame, motos_no_frame_atual


def gerencia_eventos(motos_presentes, motos_no_frame_atual, motos_desaparecidas, api_client):
    # Evento de ENTRADA: motos que estão no frame atual mas não estavam na lista de presentes
    motos_que_entraram = motos_no_frame_atual - motos_presentes
    for moto_id in motos_que_entraram:
        print(f"EVENTO [ENTRADA]: Moto {moto_id} detectada. Adicionada ao pátio.")
        motos_presentes.add(moto_id)
        motos_desaparecidas[moto_id] = 0  # Reseta o contador caso a moto retorne
        # O evento de entrada é gerenciado localmente; a API recebe o status "em_patio" a cada frame.

    # Evento de SAÍDA: motos que estavam na lista de presentes mas não estão no frame atual
    motos_potencialmente_fora = motos_presentes - motos_no_frame_atual
    for moto_id in motos_potencialmente_fora:
        motos_desaparecidas[moto_id] += 1
        
        # Confirma a saída apenas após N frames de ausência
        if motos_desaparecidas[moto_id] > FRAMES_PARA_CONFIRMAR_SAIDA:
            print(f"EVENTO [SAÍDA]: Moto {moto_id} desapareceu por {FRAMES_PARA_CONFIRMAR_SAIDA} frames. Removida do pátio.")
            motos_presentes.remove(moto_id)
            del motos_desaparecidas[moto_id]
            # Aqui você poderia chamar um endpoint específico para 'moto_saiu', se a arquitetura exigir.
            # api_client.send_event('moto_saiu', moto_id)


def main():
    # --- INICIALIZAÇÃO DOS SERVIÇOS ---
    api_client = APIClient(base_url=API_BASE_URL)
    db_manager = DatabaseManager()
    tracking_model = YOLO(TRACKING_MODEL_PATH)
    roboflow_client = InferenceHTTPClient(
        api_url=ROBOFLOW_API_URL,
        api_key=ROBOFLOW_API_KEY
    )

    # --- CONTROLE DE ESTADO ---
    motos_presentes = set()  # Guarda as motos que estão confirmadas no pátio
    motos_desaparecidas = defaultdict(int)  # Conta frames de ausência para cada moto

    # --- CONFIGURAÇÃO DO VÍDEO ---
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Erro fatal: Não foi possível abrir a fonte de vídeo: {VIDEO_SOURCE}")
        return

    print("Iniciando processamento em tempo real. Pressione 'q' na janela de vídeo para sair.")

    # --- LOOP PRINCIPAL ---
    while True:
        success, frame = cap.read()
        if not success:
            print("Fim do stream de vídeo.")
            break

        # 1. Processa o frame para detectar e rastrear as motos
        annotated_frame, motos_no_frame_atual = processa_frame(frame, tracking_model, roboflow_client, db_manager, api_client)

        # 2. Gerencia os eventos de entrada e saída
        gerencia_eventos(motos_presentes, motos_no_frame_atual, motos_desaparecidas, api_client)

        # 3. Exibe o resultado visual
        cv2.imshow("Monitoramento de Motocicletas", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Encerrando a pedido do usuário.")
            break

    # --- ENCERRAMENTO ---
    cap.release()
    cv2.destroyAllWindows()
    db_manager.close()
    print("Processamento finalizado e recursos liberados.")


if __name__ == "__main__":
    main()