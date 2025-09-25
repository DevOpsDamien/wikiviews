# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import random
import uuid

from pageviews import get_top_100, get_30day_views

# =====================
# Sous-appli "api_app"
# =====================
api_app = FastAPI()

ROUND_DATA = {}  # round_id -> {"pageA":{title,views}, "pageB":{title,views}}

class GuessPayload(BaseModel):
    roundId: str
    choice: str

@api_app.get("/round")
def new_round():
    """
    Crée un nouveau round :
    1) Récupère le top 100 du jour actuel
    2) Choisit 2 pages aléatoires
    3) Calcule leurs vues sur 30 jours
    4) Stocke en mémoire
    5) Retourne roundId + titres
    """
    top_100 = get_top_100(lang="fr")
    if not top_100:
        raise HTTPException(status_code=500, detail="Impossible de récupérer le top 100")

    # Choix aléatoire de 2 pages
    pair = random.sample(top_100, 2)
    pageA = pair[0]   # dict: {"article": "Titre", "views": ...}
    pageB = pair[1]

    viewsA = get_30day_views(pageA["article"], lang="fr")
    viewsB = get_30day_views(pageB["article"], lang="fr")

    round_id = str(uuid.uuid4())

    ROUND_DATA[round_id] = {
        "pageA": {
            "title": pageA["article"],
            "views": viewsA
        },
        "pageB": {
            "title": pageB["article"],
            "views": viewsB
        }
    }

    return {
        "roundId": round_id,
        "pages": [pageA["article"], pageB["article"]]
    }

@api_app.post("/guess")
def guess_round(data: GuessPayload):
    roundId= data.roundId
    choice = data.choice

    if roundId not in ROUND_DATA:
        raise HTTPException(status_code=404, detail="RoundID inconnu ou expiré")

    # On récupère la data
    pageA = ROUND_DATA[roundId]["pageA"]
    pageB = ROUND_DATA[roundId]["pageB"]

    winner_title = pageA["title"] if pageA["views"] >= pageB["views"] else pageB["title"]
    correct = (choice == winner_title)
    # Nettoyage pour ne pas accumuler
    del ROUND_DATA[roundId]

    return {
        "correct": correct,
        "pageA": pageA["title"],
        "viewsA": pageA["views"],
        "pageB": pageB["title"],
        "viewsB": pageB["views"]
    }

# =====================
# Appli principale
# =====================
app = FastAPI()

# On monte la sous-appli sur /api
app.mount("/api", api_app)

# On sert le dossier "client" sur la racine
app.mount("/", StaticFiles(directory="client", html=True), name="client")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

