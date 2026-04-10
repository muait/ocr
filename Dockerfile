FROM python:3.10-slim

# Installation de Tesseract OCR dans le système
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Commande pour démarrer l'app sur Render
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
