# 🏍️ Pipeline de Detecção e Identificação de Motocicletas

Este projeto implementa um pipeline de visão computacional em duas etapas para a análise de motocicletas em imagens:

**Etapa 1: Detecção de Motocicletas com YOLOv8**
Utiliza o modelo YOLOv8 para identificar e localizar motocicletas nas imagens.

**Etapa 2: Identificação de IDs com OCR**
Emprega OCR (Optical Character Recognition) para ler os números amarelos presentes nos bancos das motos detectadas, mapeando sua localização e associando o ID.

---

## 🚀 Objetivo

Automatizar o processo de análise de imagens de motocicletas, desde a detecção da presença da moto até a identificação do seu número de identificação (ID) através de OCR, gerando dados estruturados sobre a localização e os IDs encontrados.

---

## 📂 Estrutura do Projeto

motorcycle-detection/
├── imagens/
│   ├── patio.jpg                   # Imagem de entrada para detecção
│   ├── patio1.jpg                  # Outra imagem de entrada (exemplo)
├── notebooks/
│   └── iot_challenge_mottu.ipynb   # Notebook original para detecção de motos
├── src/
│   ├── detect_and_map.py          # Script Python para detecção, OCR e mapeamento
│   └── main.py                    # Script principal para execução do pipeline
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
Executar o pipeline completo
O script main.py é o ponto de entrada para executar o pipeline completo de detecção e identificação.


python src/main.py
# ou
python3 src/main.py

O main.py contém:

Executar a detecção de motocicletas (possivelmente referenciando ou incorporando a lógica do notebook original ou usando diretamente o YOLOv8).

python src/detect_and_map.py
# ou
python3 src/detect_and_map.py
Este script:

Detecta motocicletas na imagem imagens/patio.jpg.
Recorta a área dos bancos das motos.
Realiza OCR para identificar os números amarelos.
Gera a imagem anotada imagens/output.jpg.
Cria o arquivo imagens/patio_map.json com ID e coordenadas.

## 👀 Resultados
Imagem Anotada: imagens/output.jpg (mostra as motos detectadas com os IDs identificados)
Dados JSON: imagens/patio_map.json (contém os IDs das motos e suas respectivas coordenadas na imagem)
Resultado da Detecção Inicial (via main.py ou notebook): O formato e a localização dos resultados da detecção inicial (se executada separadamente) dependerão da implementação no main.py ou no notebook iot_challenge_mottu.ipynb. Geralmente, pode ser um arquivo de texto com as porcentagens de certeza da detecção das motos.

## 🛠️ Dependências Principais
Python 3.9+
ultralytics
opencv-python
pytesseract
numpy
json
matplotlib, nbformat, nbconvert, ipykernel (podem ser necessários para a execução ou referência ao notebook original)
Consulte requirements.txt para a lista completa.

## 📌 Contribuições
Sinta-se à vontade para abrir issues ou pull requests com melhorias, correções ou sugestões para o projeto.