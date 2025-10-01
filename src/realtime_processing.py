import cv2
from ultralytics import YOLO
from collections import defaultdict
from api_client import APIClient
from database import DatabaseManager

# --- PARÂMETROS DE CONFIGURAÇÃO ---
VIDEO_SOURCE = "video/video_iot.mp4"  # Use 0 para webcam (para escanear em tempo real) ou o caminho para um arquivo de vídeo
MODEL_PATH = 'yolov8n.pt'
CONFIDENCE_THRESHOLD = 0.5  # Limiar de confiança para considerar uma detecção válida
FRAMES_PARA_CONFIRMAR_SAIDA = 15  # Nº de frames que uma moto deve estar ausente para ser considerada como 'saiu'
CLASSE_ALVO = [3]  # Classe de 'motorcycle' no modelo COCO

# --- URL DA API ---
API_BASE_URL = "https://68dd9c25d7b591b4b78cea09.mockapi.io/api/v1"


def processa_frame(frame, model, db_manager):
    # Executa o rastreador do YOLO, filtrando pela classe de motocicleta
    results = model.track(frame, persist=True, classes=CLASSE_ALVO, conf=CONFIDENCE_THRESHOLD)
    
    motos_no_frame_atual = set()
    annotated_frame = results[0].plot() 

    # Se houver rastreamentos, processa cada um
    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)

        for box, track_id in zip(boxes, track_ids):
            moto_id_str = f'moto_{track_id}'
            motos_no_frame_atual.add(moto_id_str)

            # Calcula o centro da moto para registrar sua localização
            center_x = (box[0] + box[2]) // 2
            center_y = (box[1] + box[3]) // 2
            db_manager.insert_detection(moto_id_str, int(center_x), int(center_y))

    return annotated_frame, motos_no_frame_atual


def gerencia_eventos(motos_presentes, motos_no_frame_atual, motos_desaparecidas, api_client):
    # Evento de ENTRADA: motos que estão no frame atual mas não estavam na lista de presentes
    motos_que_entraram = motos_no_frame_atual - motos_presentes
    for moto_id in motos_que_entraram:
        print(f"EVENTO [ENTRADA]: Moto {moto_id} detectada. Adicionada ao pátio.")
        motos_presentes.add(moto_id)
        motos_desaparecidas[moto_id] = 0  # Reseta o contador caso a moto retorne
        api_client.send_event('moto_entrou', moto_id)

    # Evento de SAÍDA: motos que estavam na lista de presentes mas não estão no frame atual
    motos_potencialmente_fora = motos_presentes - motos_no_frame_atual
    for moto_id in motos_potencialmente_fora:
        motos_desaparecidas[moto_id] += 1
        if motos_desaparecidas[moto_id] > FRAMES_PARA_CONFIRMAR_SAIDA:
            print(f"EVENTO [SAÍDA]: Moto {moto_id} desapareceu por {FRAMES_PARA_CONFIRMAR_SAIDA} frames. Removida do pátio.")
            motos_presentes.remove(moto_id)
            del motos_desaparecidas[moto_id] 
            api_client.send_event('moto_saiu', moto_id)


def main():
    # --- INICIALIZAÇÃO DOS SERVIÇOS ---
    api_client = APIClient(base_url=API_BASE_URL)
    db_manager = DatabaseManager()
    model = YOLO(MODEL_PATH)

    # --- CONTROLE DE ESTADO ---
    # Guarda as motos que estão confirmadas no pátio
    motos_presentes = set()  
    # Conta frames de ausência para cada moto
    motos_desaparecidas = defaultdict(int)  

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
        annotated_frame, motos_no_frame_atual = processa_frame(frame, model, db_manager)

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