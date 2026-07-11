FROM python:3.12-slim

WORKDIR /app

# Installe ffmpeg (indispensable pour la génération vidéo)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copie et installe les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code
COPY . .

# Port exposé
EXPOSE 8000

# Démarre le serveur
CMD ["python3", "main.py"]
