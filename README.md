# 🏍️ Pipeline de Detecção e Identificação de Motocicletas

Este projeto implementa um pipeline de visão computacional para detecção, rastreamento e gerenciamento de motocicletas em tempo real.

**Integrantes:**

1. Eduardo Henrique Strapazzon Nagado - RM558158 
2. Felipe Silva Maciel -RM555307
3. Gustavo Ramires Lazzuri - RM556772

---

## ✨ Funcionalidades Principais

1.  **Detecção e Rastreamento em Tempo Real:** Utiliza o modelo **YOLOv8** para identificar e atribuir um ID de rastreamento único a cada motocicleta em um stream de vídeo (webcam ou arquivo).

2.  **Classificação de Modelos:** Integra-se com uma API do **Roboflow** para classificar o modelo específico de cada moto detectada (ex: `Mottu Pop`, `Mottu-E`), enriquecendo os dados coletados.

3.  **Dashboard Visual Interativo:** Exibe uma interface em tempo real com:
    - **Contagem total** de motos no pátio.
    - **Contagem por modelo** das motos visíveis.
    - **Log de eventos** de entrada e saída.
    - **Indicadores visuais:** Caixas delimitadoras mudam de cor para alertar sobre motos que estão prestes a sair do pátio.

4.  **Integração com Backend e Banco de Dados:** Envia os dados de cada detecção (ID, modelo, localização) para uma **API REST** e persiste as informações em um banco de dados **Oracle**, demonstrando um fluxo de dados ponta a ponta.

---

## 🚀 Objetivo

Automatizar o monitoramento de um pátio de motocicletas, fornecendo dados em tempo real sobre a presença, entrada e saída de veículos. O sistema gera um output visual com as detecções, registra eventos em uma API e persiste os dados para análises futuras.

---

## 📂 Estrutura do Projeto  

```bash
motorcycle-detection/
├── imagens/
│   ├── patio.jpg                   # Imagem de entrada para detecção
│   ├── patio1.jpg                  # Outra imagem de exemplo
├── notebooks/
│   └── iot_challenge_mottu.ipynb   # Notebook original de exploração
├── src/
│   ├── detect_and_map.py           # Detecção + OCR em imagens estáticas
│   ├── realtime_processing.py      # Pipeline de rastreamento em tempo real
│   ├── api_client.py               # Cliente para integração com API
│   ├── database.py                 # Conexão com banco de dados Oracle
│   └── main.py                     # Execução auxiliar do notebook
├── video/
│   └── video_iot.mp4               # Vídeo de teste para rastreamento
├── .gitignore
├── requirements.txt
└── README.md

```
---
## 🔧 Configuração do Ambiente

> ⚠️ **Importante:** Utilize um ambiente virtual para garantir o correto funcionamento das dependências.

### 1. Clone o repositório


git clone [https://github.com/fesilva2109/mottu_challenge_iot.git](https://github.com/fesilva2109/mottu_challenge_iot.git)

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

pip install -r requirements.txt -v
# ou
pip3 install -r requirements.txt -v

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
- Exibir o dashboard visual com contadores, logs e indicadores.
- Imprimir no console os eventos de entrada e saída.
- Enviar os dados para a API configurada.
- Registrar cada detecção em um banco de dados Oracle (se as credenciais estiverem configuradas).

---
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

*   **Dashboard em Tempo Real:** Uma janela de vídeo mostrando o dashboard com as motos rastreadas, contadores, logs e indicadores visuais.
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


## 📹 Vídeo Youtube 
* VIDEO: https://youtu.be/vFNWEzWuZ0c?si=c3iqPxp814yybjNo
