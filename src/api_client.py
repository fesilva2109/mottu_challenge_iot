#pip install requests
import requests
import json
from datetime import datetime

class APIClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url

    def send_detection_event(self, moto_id, model_name, center_x, center_y, status="em_patio"):
        endpoint = f"{self.base_url}/detections" # Conforme a arquitetura
        payload = {
            "motoId": moto_id,
            "modelo": model_name,
            "centerX": center_x,
            "centerY": center_y,
            "timestamp": datetime.now().isoformat(),
            "status": status
        }

        print(f"Enviando para API: {payload}")

        try:
            # Envia o evento para a API real
            response = requests.post(endpoint, json=payload, timeout=5) # Timeout para evitar travamentos
            
            # Status 201 (Created) é o esperado para um POST bem-sucedido
            if response.status_code == 201:
                print("✅ Evento registrado com sucesso pela API.")
            else:
                print(f"⚠️ API retornou um status inesperado: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao comunicar com a API ({endpoint}): {e}")

    # O método send_event original não é mais usado para detecções contínuas
    # mas pode ser mantido ou adaptado para outros tipos de eventos se necessário.
    # Por enquanto, focaremos no send_detection_event para o POST /detections.
    def send_event(self, event_type, moto_id):
        print(f"⚠️ O método send_event foi substituído por send_detection_event para o fluxo de detecções. Evento '{event_type}' para '{moto_id}' não enviado via API.")