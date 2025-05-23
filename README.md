# 🏍️ Motorcycle Detection with YOLOv8

Este projeto utiliza o modelo YOLOv8 para realizar a **detecção automática de motocicletas** em imagens.

---

## 🚀 Objetivo

Automatizar a execução do notebook `iot_challenge_mottu.ipynb` com um script Python para facilitar testes e reprodutibilidade do pipeline de detecção de motocicletas.

---

## 🔧 Configuração do Ambiente (Obrigatório)

> ⚠️ **ATENÇÃO:** É obrigatório usar um ambiente virtual para garantir que as dependências funcionem corretamente.

### 1. Clone o repositório

git clone https://github.com/fesilva2109/mottu_challenge_iot.git
cd motorcycle-detection

### 2. Crie um ambiente virtual Python
python -m venv .venv
ou
python3 -m venv .venv

### 3. Ative o ambiente virtual
No macOS/Linux:
source .venv/bin/activate

No Windows (cmd):
.venv\Scripts\activate

### 4. Instale as dependências4. Instale as dependências
pip install -r requirements.txt
ou
pip3 install -r requirements.txt

### 5. Instale o ipykernel
pip install ipykernel

### 6. Registre o kernel no Jupyter:
python -m ipykernel install --user --name=python3

### 7. Rodar a Main
python src/main.py
ou
python3 src/main.py

### Visualizando o Resultado
Para verificar se as imagens foram corretamente categorizadas como motos, acesse a pasta "imagens" na aba de notebooks. Lá, em um arquivo gerado, você encontrará a porcentagem de certeza com que o modelo classificou cada figura como uma moto.


### 🛠️ Dependências Principais
Python 3.9+ 

nbformat

nbconvert

ultralytics

opencv-python

matplotlib

Veja a lista completa no arquivo requirements.txt.
