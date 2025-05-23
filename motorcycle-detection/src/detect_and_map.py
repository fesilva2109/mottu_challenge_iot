import logging
from ultralytics import YOLO
import cv2
import pytesseract
import json
import os
import numpy as np

# Configuração do logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Caminhos
IMG_PATH = 'imagens/patio.jpg'
OUTPUT_IMG = 'imagens/output.jpg'
JSON_PATH = 'imagens/patio_map.json'

logging.debug(f"Caminho da imagem: {IMG_PATH}")
logging.debug(f"Caminho da imagem de saída: {OUTPUT_IMG}")
logging.debug(f"Caminho do arquivo JSON: {JSON_PATH}")

try:
    # Carrega modelo YOLOv8
    logging.info("Carregando modelo YOLOv8...")
    model = YOLO('yolov8n.pt')
    logging.info("Modelo YOLOv8 carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo YOLOv8: {e}")
    exit()

try:
    # Detecta motos
    logging.info("Detectando motos na imagem...")
    results = model(IMG_PATH)[0]
    logging.info(f"Detecção de motos concluída. {len(results.boxes)} motos encontradas.")
except Exception as e:
    logging.error(f"Erro durante a detecção de motos: {e}")
    exit()

# Lista para o JSON
motos_detectadas = []

try:
    # Carrega imagem original
    logging.info("Carregando imagem original...")
    image = cv2.imread(IMG_PATH)
    if image is None:
        logging.error(f"Erro ao carregar a imagem: {IMG_PATH}. Verifique se o arquivo existe.")
        exit()
    logging.info("Imagem original carregada com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar a imagem original: {e}")
    exit()

for i, box in enumerate(results.boxes):
    try:
        cls = int(box.cls)
        conf = float(box.conf)
        logging.debug(f"Moto {i}: Classe={cls}, Confiança={conf}")
        if cls != 3:  # classe 3 = motorcycle no COCO
            logging.debug(f"Moto {i}: Classe não é 3 (motocicleta). Ignorando.")
            continue

        x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
        logging.debug(f"Moto {i}: Coordenadas da bounding box (x1={x1}, y1={y1}, x2={x2}, y2={y2})")
        cropped_moto = image[y1:y2, x1:x2].copy()

        # Recorte da área do número com mais precisão (ajuste conforme necessário)
        height_cropped_start = int((y2 - y1) * 0.5)  # Começar na metade da altura
        height_cropped_end = int((y2 - y1) * 0.8)    # Estender até 80% da altura
        cropped_number_area = cropped_moto[height_cropped_start:height_cropped_end, :]
        logging.debug(f"Moto {i}: Área do número recortada.")
        cv2.imwrite(f"debug_cropped_number_{i}.jpg", cropped_number_area)

        try:
            # Pré-processamento focado na cor amarela e contraste
            hsv_cropped = cv2.cvtColor(cropped_number_area, cv2.COLOR_BGR2HSV)

            # Definir uma faixa mais específica para a cor amarela
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            mask_yellow = cv2.inRange(hsv_cropped, lower_yellow, upper_yellow)
            yellow_only = cv2.bitwise_and(cropped_number_area, cropped_number_area, mask=mask_yellow)
            gray_yellow = cv2.cvtColor(yellow_only, cv2.COLOR_BGR2GRAY)

            # Aplicar um threshold para criar um contraste acentuado
            _, binary_yellow = cv2.threshold(gray_yellow, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Aumentar o tamanho para melhor leitura
            resized_binary = cv2.resize(binary_yellow, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

            logging.info(f"Moto {i}: Iniciando OCR...")
            numero = pytesseract.image_to_string(resized_binary, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
            logging.debug(f"Moto {i}: Resultado do OCR (antes da limpeza): '{numero}'")

            numero = ''.join(filter(str.isdigit, numero))
            logging.debug(f"Moto {i}: Resultado do OCR (após a limpeza): '{numero}'")

        except Exception as e:
            logging.error(f"Moto {i}: Erro durante o OCR: {e}")
            numero = None

        moto_id = numero if numero else f'moto_{i}'
        motos_detectadas.append({
            'id': moto_id,
            'x': (x1 + x2) // 2,
            'y': (y1 + y2) // 2,
        })
        logging.info(f"Moto {i}: Adicionada à lista com ID '{moto_id}', centro x={(x1 + x2) // 2}, centro y={(y1 + y2) // 2}")

        label = numero if numero else f'#{i}'
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        logging.debug(f"Moto {i}: Desenho da bounding box e label na imagem.")

    except Exception as e:
        logging.error(f"Erro ao processar a moto {i}: {e}")

try:
    logging.info(f"Salvando imagem anotada em: {OUTPUT_IMG}")
    cv2.imwrite(OUTPUT_IMG, image)
    logging.info("Imagem anotada salva com sucesso.")
except Exception as e:
    logging.error(f"Erro ao salvar a imagem anotada: {e}")

try:
    logging.info(f"Salvando dados JSON em: {JSON_PATH}")
    with open(JSON_PATH, 'w') as f:
        json.dump({'motos': motos_detectadas}, f, indent=2)
    logging.info("Dados JSON salvos com sucesso.")
except Exception as e:
    logging.error(f"Erro ao salvar o arquivo JSON: {e}")

print(f'Detectadas {len(motos_detectadas)} motos.')
logging.info(f"Script finalizado. Total de {len(motos_detectadas)} motos detectadas.")