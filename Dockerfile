# 1) Choix d’une image Python légère
FROM arm32v7/python:3.9-slim

# 2) Créer un dossier d’appli
WORKDIR /app

# 3) Copier les fichiers requirements (si tu en as un)
#    Ou on va pip install direct
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copier le reste du code
COPY . .

# 5) Exposer le port 8000
EXPOSE 8000

# 6) Lancer l’appli via uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

