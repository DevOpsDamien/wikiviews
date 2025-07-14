# pageviews.py
import requests
from datetime import datetime, timedelta

# Un User-Agent personnalisé est OBLIGATOIRE pour respecter la politique Wikimedia
USER_AGENT = "TimelineGame/1.0 (User: damien; email: H2O.damien@proton.me)"

def get_top_100(lang="fr"):
    """
    Récupère le top (jusqu'à 100) des articles Wikipédia le JOUR ACTUEL (selon UTC).
    ATTENTION : si la journée n'est pas terminée, il se peut que l'API ne renvoie pas de données.
    """
    # On récupère la date du jour (UTC)
    today = (datetime.utcnow().date() - timedelta(days=1))
    year = today.year
    month = today.month
    day = today.day

    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{lang}.wikipedia/all-access/{year}/{month:02d}/{day:02d}"
    print("[DEBUG] get_top_100 URL =", url)

    # On ajoute un header User-Agent
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[ERROR] Top 100 request failed: {response.status_code} - {response.text}")
        return []

    data = response.json()
    items = data.get("items", [])
    if not items:
        return []

    # items[0]["articles"] contient le classement, on prend les 100 premiers
    articles = items[0].get("articles", [])
    top_100 = articles[:100]
    return top_100

def get_30day_views(article_title, lang="fr"):
    """
    Calcule la somme des vues sur les 30 derniers jours pour 'article_title'.
    Retourne 0 si erreur.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)

    end_str = end_date.strftime('%Y%m%d00')   # ex: 2023040100
    start_str = start_date.strftime('%Y%m%d00')

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"{lang}.wikipedia/all-access/all-agents/{article_title}/daily/"
        f"{start_str}/{end_str}"
    )
    print("[DEBUG] get_30day_views URL =", url)

    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"[ERROR] 30-day views request failed: {resp.status_code} - {resp.text}")
        return 0

    data = resp.json()
    items = data.get("items", [])
    total_views = sum(item["views"] for item in items)
    return total_views

