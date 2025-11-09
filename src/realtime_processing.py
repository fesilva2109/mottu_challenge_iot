import cv2
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient
from collections import defaultdict, deque
from api_client import APIClient
from database import DatabaseManager

# --- PARÂMETROS DE CONFIGURAÇÃO ---
VIDEO_SOURCE = 0  # 0 para webcam ou caminho para um arquivo de vídeo
TRACKING_MODEL_PATH = 'yolov8n.pt'
TRACKING_CLASS_ID = [3]  # Classe 'motorcycle'
ROBOFLOW_API_URL = "https://detect.roboflow.com"
ROBOFLOW_API_KEY = "aFBnNsh545I9GTlTUzpa"
ROBOFLOW_MODEL_ID = "mottu-iot-iycbr/1"
CONFIDENCE_THRESHOLD = 0.5
CLASSIFICATION_CONFIDENCE_THRESHOLD = 0.80
FRAMES_PARA_CONFIRMAR_SAIDA = 15
DASHBOARD_HEIGHT = 120
MAX_LOG_ENTRIES = 4
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
    

def processa_frame(frame, tracking_model, roboflow_client, db_manager, api_client, motos_desaparecidas):
    results = tracking_model.track(frame, persist=True, classes=TRACKING_CLASS_ID, conf=CONFIDENCE_THRESHOLD)

    motos_no_frame_atual = set()
    contagem_modelos = defaultdict(int)
    annotated_frame = frame.copy()

    total_motos_detectadas = 0

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)

        for i, (box, track_id) in enumerate(zip(boxes, track_ids)):
            moto_id_str = f'moto_{track_id}'
            motos_no_frame_atual.add(moto_id_str)
            total_motos_detectadas += 1

            x1, y1, x2, y2 = box
            cropped_moto = frame[y1:y2, x1:x2]
            classification_result = roboflow_client.infer(cropped_moto, model_id=ROBOFLOW_MODEL_ID)

            predictions = classification_result.get('predictions', [])
            model_name = 'Analisando...'
            
            if predictions:
                top_prediction = predictions[0]
                confidence = top_prediction.get('confidence', 0)

                if confidence >= CLASSIFICATION_CONFIDENCE_THRESHOLD:
                    raw_model_name = top_prediction['class']
                    model_name = format_model_name(raw_model_name)
                    contagem_modelos[model_name] += 1
                    
                    center_x = (box[0] + box[2]) // 2
                    center_y = (box[1] + box[3]) // 2

                    db_manager.insert_detection(moto_id_str, int(center_x), int(center_y), model_name)
                    api_client.send_detection_event(moto_id_str, model_name, int(center_x), int(center_y), status="em_patio")
                else:
                    model_name = 'Modelo Incerto'  # Se a confiança for baixa, apenas exibe na tela

            cor_caixa = (0, 255, 0)  # Verde (Normal)
            if moto_id_str in motos_desaparecidas and motos_desaparecidas[moto_id_str] > 0:
                cor_caixa = (0, 255, 255)  # Amarelo (Atenção)

            label = f"ID: {track_id} - {model_name}"
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), cor_caixa, 2)
            cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_caixa, 2)

    return annotated_frame, motos_no_frame_atual, total_motos_detectadas, contagem_modelos

def gerencia_eventos(motos_presentes, motos_no_frame_atual, motos_desaparecidas, log_eventos, api_client):
    motos_que_entraram = motos_no_frame_atual - motos_presentes
    for moto_id in motos_que_entraram:
        msg = f"ENTRADA: {moto_id} detectada."
        print(f"EVENTO [{msg}]")
        log_eventos.appendleft(msg)
        motos_presentes.add(moto_id)
        motos_desaparecidas[moto_id] = 0

    motos_potencialmente_fora = motos_presentes - motos_no_frame_atual
    
    for moto_id in motos_presentes.intersection(motos_no_frame_atual):
        if motos_desaparecidas[moto_id] > 0:
            motos_desaparecidas[moto_id] = 0

    for moto_id in motos_potencialmente_fora:
        motos_desaparecidas[moto_id] += 1
        
        if motos_desaparecidas[moto_id] > FRAMES_PARA_CONFIRMAR_SAIDA:
            msg = f"SAIDA: {moto_id} confirmada."
            print(f"EVENTO [{msg}]")
            log_eventos.appendleft(msg)
            motos_presentes.remove(moto_id)
            del motos_desaparecidas[moto_id]


def main():
    api_client = APIClient(base_url=API_BASE_URL)
    db_manager = DatabaseManager()
    tracking_model = YOLO(TRACKING_MODEL_PATH)
    roboflow_client = InferenceHTTPClient(
        api_url=ROBOFLOW_API_URL,
        api_key=ROBOFLOW_API_KEY
    )

    motos_presentes = set()
    motos_desaparecidas = defaultdict(int)
    log_eventos = deque(maxlen=MAX_LOG_ENTRIES)

    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Erro fatal: Não foi possível abrir a fonte de vídeo: {VIDEO_SOURCE}")
        return

    print("Iniciando processamento em tempo real. Pressione 'q' na janela de vídeo para sair.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Fim do stream de vídeo.")
            break

        h, w, _ = frame.shape
        dashboard_frame = cv2.copyMakeBorder(frame, DASHBOARD_HEIGHT, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        annotated_frame, motos_no_frame_atual, total_motos, contagem_modelos = processa_frame(
            frame, tracking_model, roboflow_client, db_manager, api_client, motos_desaparecidas
        )

        gerencia_eventos(motos_presentes, motos_no_frame_atual, motos_desaparecidas, log_eventos, api_client)

        dashboard_frame[DASHBOARD_HEIGHT:, :, :] = annotated_frame

        cv2.putText(dashboard_frame, f"Total de Motos no Patio: {len(motos_presentes)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        modelos_str = ", ".join([f"{modelo}: {qtd}" for modelo, qtd in contagem_modelos.items()])
        cv2.putText(dashboard_frame, f"Modelos Detectados: {modelos_str}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        cv2.putText(dashboard_frame, "Log de Eventos:", (w - 300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        for i, log_msg in enumerate(log_eventos):
            cv2.putText(dashboard_frame, log_msg, (w - 300, 60 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255) if "ENTRADA" in log_msg else (0, 0, 255), 2)

        cv2.imshow("Monitoramento de Motocicletas - Mottu Challenge", dashboard_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Encerrando a pedido do usuário.")
            break

    cap.release()
    cv2.destroyAllWindows()
    db_manager.close()
    print("Processamento finalizado e recursos liberados.")


if __name__ == "__main__":
    main()