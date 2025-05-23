# 🏍️ Detecção e Mapeamento de Motocicletas com YOLOv8 e OCR

Este projeto utiliza o modelo YOLOv8 para realizar a **detecção automática de motocicletas** em imagens e, adicionalmente, emprega **OCR (Optical Character Recognition)** para identificar os números amarelos presentes nos bancos das motos, mapeando sua localização.

---

## 🚀 Objetivo

Automatizar a detecção de motocicletas em imagens, identificar os números de identificação (amarelos) utilizando OCR e gerar um arquivo JSON contendo a localização das motos e seus respectivos IDs (quando identificados).

---

## 📂 Estrutura do Projeto

```

motorcycle-detection/
├── imagens/
│   ├── patio.jpg                   # Imagem de entrada para detecção
│   ├── patio1.jpg                  # Outra imagem de entrada (exemplo)
├── notebooks/
│   └── iot\_challenge\_mottu.ipynb   # Notebook original
├── src/
│   ├── detect\_and\_map.py          # Script de detecção, OCR e mapeamento
│   └── main.py                    # Script principal para execução (opcional)
├── .gitignore
├── requirements.txt
└── README.md

````

---

## 🔧 Configuração do Ambiente

> ⚠️ **Importante:** Utilize um ambiente virtual para garantir o correto funcionamento das dependências.

### 1. Clone o repositório

```bash
git clone https://github.com/fesilva2109/mottu_challenge_iot.git
cd motorcycle-detection
````

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
# ou
python3 -m venv .venv
```

### 3. Ative o ambiente virtual

* **macOS/Linux:**

  ```bash
  source .venv/bin/activate
  ```

* **Windows (cmd):**

  ```bash
  .venv\Scripts\activate
  ```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
# ou
pip3 install -r requirements.txt
```

### 5. Instale o Tesseract OCR

**macOS (via Homebrew):**

```bash
brew install tesseract
brew install tesseract-lang
```

**Linux (Debian/Ubuntu):**

```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-eng
```

**Windows:**

Baixe o instalador em: [UB Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

Certifique-se de adicionar `tesseract.exe` ao PATH do sistema.

---

## ▶️ Execução

### Executar o script principal

```bash
python src/detect_and_map.py
# ou
python3 src/detect_and_map.py
```

Este script:

* Detecta motocicletas na imagem `imagens/patio.jpg`.
* Recorta a área dos bancos das motos.
* Realiza OCR para identificar os números amarelos.
* Gera a imagem anotada `imagens/output.jpg`.
* Cria o arquivo `imagens/patio_map.json` com ID e coordenadas.

### Rodar o `main.py` (se aplicável)

```bash
python src/main.py
```

Verifique se esse arquivo ainda é necessário e mantenha atualizado conforme o uso.

---

## 👀 Resultados

* **Imagem Anotada:** `imagens/output.jpg`
* **Dados JSON:** `imagens/patio_map.json` (contém IDs e localização das motos)

---

## 🛠️ Dependências Principais

* Python 3.9+
* [`ultralytics`](https://pypi.org/project/ultralytics/)
* `opencv-python`
* `pytesseract`
* `numpy`
* `json`
* `matplotlib`, `nbformat`, `nbconvert` (para o notebook)

Consulte `requirements.txt` para a lista completa.

---

## 📌 Contribuições

Sinta-se à vontade para abrir *issues* ou *pull requests* com melhorias, correções ou sugestões para o projeto.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

```

---

Se quiser, posso te ajudar a criar um `LICENSE`, um badge do GitHub ou um GIF demonstrando o funcionamento. Deseja incluir algo mais?
```