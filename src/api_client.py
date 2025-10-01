#pip install requests
import requests
import json
from datetime import datetime

class APIClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url

    def send_event(self, event_type, moto_id):
        endpoint = f"{self.base_url}/events"
        payload = {
            "event_type": event_type, # 'moto_entrou' ou 'moto_saiu'
            "moto_id": moto_id,
            "timestamp": datetime.now().isoformat()
        }

        print(f"Enviando para API: {payload}")

        try:
            # Envia o evento para a API real
            response = requests.post(endpoint, json=payload, timeout=5)
            response.raise_for_status() # Lança um erro para status codes 4xx/5xx
            
            # Status 201 (Created) é o esperado para um POST bem-sucedido
            if response.status_code == 201:
                print("✅ Evento registrado com sucesso pela API.")
            else:
                print(f"⚠️ API retornou um status inesperado: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Erro ao comunicar com a API: {e}")