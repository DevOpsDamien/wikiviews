FROM python:3.9-slim

# 1) Créer le dossier de travail
WORKDIR /app

# 2) Installer dépendances
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copier le backend
COPY app/ .

# 4) Copier le frontend (sera servi par FastAPI via StaticFiles)
COPY client/ ./client/

# 5) Exposer le port
EXPOSE 8000

# 6) Lancer l’app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

