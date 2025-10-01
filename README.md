# 🏍️ Pipeline de Detecção e Identificação de Motocicletas

Este projeto implementa um pipeline de visão computacional para detecção, rastreamento e gerenciamento de motocicletas em tempo real.

**Funcionalidades Principais:**

1.  **Detecção e Rastreamento em Tempo Real:** Utiliza o modelo YOLOv8 para identificar e rastrear múltiplas motocicletas em um stream de vídeo (câmera ou arquivo). A cada moto é atribuído um ID de rastreamento único.

2.  **Registro de Eventos (Entrada/Saída):** O sistema detecta quando uma nova moto entra no campo de visão e quando uma moto sai, simulando o envio desses eventos para um backend via API.

3.  **Persistência de Dados:** O histórico de detecções (ID da moto e sua localização) é registrado em um banco de dados Oracle, criando um registro persistente da presença das motos.

4.  **Análise de Imagem Estática (Funcionalidade Original):**
    - **Detecção com YOLOv8:** Identifica motocicletas em uma imagem estática.
    - **Identificação de IDs com OCR:** Emprega OCR para ler os números amarelos nos bancos das motos detectadas, mapeando sua localização e associando o ID.

---

## 🚀 Objetivo

Automatizar o monitoramento de um pátio de motocicletas, fornecendo dados em tempo real sobre a presença, entrada e saída de veículos. O sistema gera um output visual com as detecções, registra eventos em uma API e persiste os dados para análises futuras.

---

## 📂 Estrutura do Projeto

motorcycle-detection/
├── imagens/
│   ├── patio.jpg                   # Imagem de entrada para detecção
│   ├── patio1.jpg                  # Outra imagem de entrada (exemplo)
├── notebooks/
│   └── iot_challenge_mottu.ipynb   # Notebook original para exploração e detecção
├── src/
│   ├── detect_and_map.py           # Script para análise de imagem estática (detecção + OCR)
│   ├── realtime_processing.py      # Script principal para rastreamento em tempo real e registro de eventos
│   ├── api_client.py               # Módulo cliente para comunicação com API (simulado)
│   ├── database.py                 # Módulo de gerenciamento de conexão com o banco de dados
│   └── main.py                     # Script auxiliar para executar o notebook
├── video/
│   └── video_iot.mp4               # Vídeo de entrada para rastreamento em tempo real
├── .gitignore
├── requirements.txt
└── README.md


---

## 🔧 Configuração do Ambiente

> ⚠️ **Importante:** Utilize um ambiente virtual para garantir o correto funcionamento das dependências.

### 1. Clone o repositório


git clone [https://github.com/fesilva2109/mottu_challenge_iot.git](https://github.com/fesilva2109/mottu_challenge_iot.git)
cd motorcycle-detection

### 2. Crie um ambiente virtual

python -m venv .venv
# ou
python3 -m venv .venv

### 3. Ative o ambiente virtual
macOS/Linux:


source .venv/bin/activate
Windows (cmd):

.venv\Scripts\activate

### 4. Instale as dependências

pip install -r requirements.txt
# ou
pip3 install -r requirements.txt

### 5. Instale o Tesseract OCR
macOS (via Homebrew):

brew install tesseract
brew install tesseract-lang

Linux (Debian/Ubuntu):

sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-eng

Windows:

Baixe o instalador em: UB Mannheim Tesseract OCR

Certifique-se de adicionar tesseract.exe ao PATH do sistema.


### 6. Instale o pytesseract e uma versão compatível do numpy
Devido a possíveis incompatibilidades com versões mais recentes do numpy, é recomendado instalar uma versão específica e o pytesseract para o correto funcionamento do OCR.


pip install pytesseract
pip install numpy==1.26.4
# ou
pip3 install pytesseract
pip3 install numpy==1.26.4

## ▶️ Execução

### 1. Executar o Pipeline de Tempo Real 

O script `realtime_processing.py` é o ponto de entrada para a funcionalidade de rastreamento em tempo real. Ele ativa a webcam por padrão.

```bash
python src/realtime_processing.py
```

Este script irá:
- Iniciar a detecção e rastreamento de motos via webcam.
- Exibir um output visual com as motos detectadas e seus IDs de rastreamento.
- Imprimir no console os eventos de "moto entrou" e "moto saiu".
- Tentar registrar cada detecção em um banco de dados Oracle (requer configuração de credenciais).


### 2. Executar a Análise de Imagem Estática 

```bash
python src/detect_and_map.py
```
Este script:
Detecta motocicletas na imagem imagens/patio.jpg.
Recorta a área dos bancos das motos.
Realiza OCR para identificar os números amarelos.
Gera a imagem anotada imagens/output.jpg.
Cria o arquivo imagens/patio_map.json com ID e coordenadas.

## 👀 Resultados

*   **Output Visual em Tempo Real:** Uma janela de vídeo mostrando as motos rastreadas com suas caixas delimitadoras e IDs.
*   **Logs de Eventos no Console:** Mensagens como `EVENTO [ENTRADA]: Moto moto_1 detectada.` e `EVENTO [SAÍDA]: Moto moto_1 desapareceu.`.
*   **Banco de Dados:** (Se configurado) A tabela `Detections` será populada com o histórico de localizações das motos.
*   **Resultados da Análise Estática:**
    - **Imagem Anotada:** `imagens/output.jpg` (mostra as motos detectadas com os IDs do OCR).
    - **Dados JSON:** `imagens/patio_map.json` (contém os IDs do OCR e suas coordenadas).

## 🛠️ Dependências Principais
Python 3.9+
ultralytics
opencv-python
pytesseract
numpy
requests
oracledb
Consulte requirements.txt para a lista completa.

## 📌 Contribuições
Sinta-se à vontade para abrir issues ou pull requests com melhorias, correções ou sugestões para o projeto.
