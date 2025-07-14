# WikiViews (Useless Comparator)

**WikiViews** est une application web ludique qui vous met au défi de deviner laquelle de deux pages Wikipédia francophones est la plus populaire sur les 30 derniers jours.

---

## Fonctionnalités principales

- **Récupération du Top 100** : utilise l’API Wikimedia pour interroger le classement des 100 articles les plus consultés en français (REST API Metrics Pageviews).  
- **Comparaison de popularité** : sélection aléatoire de deux articles, calcul de leur nombre total de vues sur les 30 derniers jours.  
- **Back-end Python / FastAPI** : deux points d’entrée REST –  
  - **GET /api/round** : démarre une nouvelle manche, renvoie un `roundId` et la paire de titres.  
  - **POST /api/guess** : reçoit `{ roundId, choice }`, répond `{ correct, pageA, viewsA, pageB, viewsB }`.  
- **Front-end statique** : interface JavaScript/HTML/CSS minimaliste (dossier `client/`), servie directement par FastAPI.  
- **Docker & Kubernetes** : Dockerfile optimisé pour ARM32 Python 3.9, manifest Kubernetes (`deployment.yaml`) inclus.

---

## Prérequis

- **Python 3.9+**  
- **pip**  
- **Docker** (optionnel pour conteneurisation)  
- Connexion Internet (accès à l’API Wikimedia)

---
