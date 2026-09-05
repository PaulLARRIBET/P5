# Futurisys ML API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-pytest-success.svg)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://www.docker.com/)
[![Deploy](https://img.shields.io/badge/deploy-Render-46E3B7.svg)](https://render.com/)

## Présentation

Ce projet est un **Proof of Concept** réalisé dans le cadre d’un projet OpenClassrooms.

L’objectif est de rendre un modèle de machine learning opérationnel et accessible via une API, tout en mettant en place des pratiques d’ingénierie logicielle adaptées à un projet de déploiement ML :

- exposition du modèle via **FastAPI** ;
- validation des entrées avec **Pydantic** ;
- tests automatisés avec **Pytest** ;
- persistance des prédictions dans **PostgreSQL** ;
- gestion du code avec **Git / GitHub** ;
- conteneurisation avec **Docker** ;
- intégration continue avec **GitHub Actions** ;
- déploiement automatique sur **Render**.

Le modèle utilisé est un **XGBoost Classifier** permettant de prédire le départ potentiel d’un employé.

---

## Architecture du projet

```text
P5/
├── .github/
│   └── workflows/
│       └── ci.yml
├── models/
│   ├── best_xgb.pkl
│   └── preprocessor.pkl
├── scripts/
├── sql/
│   └── create_tables.sql
├── src/
│   └── p5/
│       ├── __init__.py
│       ├── app.py
│       ├── config.py
│       ├── database.py
│       ├── model.py
│       └── schemas.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Stack technique

| Domaine | Technologie |
|---|---|
| Langage | Python 3.12 |
| API | FastAPI |
| Validation | Pydantic |
| Modèle ML | XGBoost |
| Préprocessing | Scikit-learn |
| Manipulation de données | Pandas / NumPy |
| Base de données | PostgreSQL |
| Accès base | SQLAlchemy |
| Tests | Pytest / pytest-cov |
| Conteneurisation | Docker |
| Versioning | Git / GitHub |
| CI/CD | GitHub Actions |
| Hébergement | Render |
| Gestion des dépendances | uv |

---

## Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/PaulLARRIBET/P5.git
cd P5
```

### 2. Installer les dépendances

```bash
uv sync
```

### 3. Activer l’environnement virtuel

```bash
source .venv/bin/activate
```

---

## Variables d’environnement

Créer un fichier `.env` à la racine du projet.

Exemple :

```env
DATABASE_URL=postgresql://paullarribet@localhost:5432/p5
```

Le fichier `.env` est ignoré par Git afin d’éviter d’exposer des informations sensibles.

Un fichier `.env.example` est fourni comme modèle.

---

## Base de données PostgreSQL

Le projet utilise PostgreSQL pour enregistrer les appels au modèle.

La table principale est créée via :

```text
sql/create_tables.sql
```

Structure :

```sql
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_data JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    probability DOUBLE PRECISION NOT NULL
);
```

Chaque prédiction conserve :

- les données d’entrée ;
- la classe prédite ;
- la probabilité associée ;
- la date de création.

### Création locale de la base

```bash
createdb p5
psql p5
```

Puis dans `psql` :

```sql
\i /chemin/vers/P5/sql/create_tables.sql
```

---

## Lancer l’API en local

Depuis la racine du projet :

```bash
uv run uvicorn p5.app:app --app-dir src --reload
```

API :

```text
http://127.0.0.1:8000
```

Swagger :

```text
http://127.0.0.1:8000/docs
```

---

## Endpoints

### `GET /`

Vérifie que l’application répond.

Exemple :

```json
{
  "message": "Futurisys ML API is running"
}
```

### `GET /health`

Endpoint de contrôle simple.

Exemple :

```json
{
  "status": "ok"
}
```

### `POST /predict`

Retourne la prédiction du modèle et sa probabilité.

Exemple de payload :

```json
{
  "genre": "F",
  "statut_marital": "Célibataire",
  "departement": "Consulting",
  "poste": "Cadre Commercial",
  "heure_supplementaires": "Oui",
  "domaine_etude": "Infra & Cloud",
  "frequence_deplacement": "Aucun",
  "age": 35,
  "revenu_mensuel": 3000,
  "nombre_experiences_precedentes": 2,
  "annee_experience_totale": 10,
  "annees_dans_l_entreprise": 5,
  "annees_dans_le_poste_actuel": 2,
  "satisfaction_employee_environnement": 3,
  "note_evaluation_precedente": 3,
  "niveau_hierarchique_poste": 2,
  "satisfaction_employee_nature_travail": 3,
  "satisfaction_employee_equipe": 4,
  "satisfaction_employee_equilibre_pro_perso": 3,
  "note_evaluation_actuelle": 4,
  "augementation_salaire_precedente": 12,
  "nombre_participation_pee": 1,
  "nb_formations_suivies": 2,
  "distance_domicile_travail": 15,
  "niveau_education": 3,
  "annees_depuis_la_derniere_promotion": 1,
  "annes_sous_responsable_actuel": 2
}
```

Exemple de réponse :

```json
{
  "prediction": 1,
  "probability": 0.587685227394104
}
```

---

## Modèle de machine learning

Le modèle utilisé est un `XGBClassifier` entraîné en amont.

Deux fichiers sont chargés par l’API :

```text
models/best_xgb.pkl
models/preprocessor.pkl
```

- `best_xgb.pkl` contient le modèle entraîné ;
- `preprocessor.pkl` contient le préprocesseur Scikit-learn ajusté sur les données d’entraînement.

En production, l’API applique uniquement :

```python
preprocessor.transform(...)
```

Le préprocesseur n’est jamais réentraîné lors d’une requête.

---

## Feature engineering

Avant la prédiction, l’API recrée les variables dérivées utilisées pendant l’entraînement :

- `ratio_poste_entreprise`
- `ratio_promotion_entreprise`
- `ratio_manager_entreprise`
- `revenu_par_experience`
- `mobilite_carriere`

Cela garantit que le modèle reçoit le même espace de features qu’au moment de son entraînement.

---

## Validation des entrées

Pydantic valide les données avant leur passage au modèle.

Exemple pour une variable catégorielle :

```python
genre: Literal["F", "M"]
```

Exemple pour une variable numérique :

```python
age: int = Field(ge=0, le=100)
```

Une requête invalide retourne automatiquement une erreur HTTP `422`.

---

## Tests

Les tests sont écrits avec Pytest.

Ils couvrent notamment :

- l’endpoint `/health` ;
- une prédiction valide ;
- une catégorie invalide ;
- une valeur numérique hors limites ;
- les scénarios de validation Pydantic.

Lancer les tests :

```bash
PYTHONPATH=src uv run pytest tests -v
```

---

## Couverture de tests

Générer le rapport :

```bash
PYTHONPATH=src uv run pytest --cov=src/p5 --cov-report=term-missing
```

Couverture obtenue lors du développement :

```text
97 %
```

---

## Docker

### Construire l’image

```bash
docker build -t p5-api .
```

### Lancer le conteneur

```bash
docker run --rm \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql://user:password@host:5432/p5" \
  p5-api
```

L’API est alors disponible sur :

```text
http://127.0.0.1:7860
```

Swagger :

```text
http://127.0.0.1:7860/docs
```

---

## Déploiement

L’application est déployée sur Render.

### API en ligne

https://p5-tqd4.onrender.com

### Documentation Swagger

https://p5-tqd4.onrender.com/docs

La base PostgreSQL utilisée par l’environnement déployé est également hébergée sur Render.

La variable `DATABASE_URL` est injectée via les variables d’environnement Render.

---

## CI/CD

Le pipeline GitHub Actions est défini dans :

```text
.github/workflows/ci.yml
```

### Pipeline de validation

```text
Pull Request / Push
        ↓
Installation de Python
        ↓
Installation des dépendances
        ↓
Démarrage d'un PostgreSQL de test
        ↓
Création des tables
        ↓
Exécution de Pytest
        ↓
Validation du pipeline
```

### Pipeline de déploiement

Lors d’un push sur `develop` :

```text
Push sur develop
        ↓
Tests automatiques
        ↓
Tests réussis
        ↓
Déclenchement du Deploy Hook Render
        ↓
Nouvelle version déployée
```

Le déploiement dépend du succès du job de tests.

---

## Gestion des secrets

Les secrets ne sont pas enregistrés dans le dépôt.

Ils sont gérés via :

- `.env` en local ;
- **GitHub Secrets** pour le pipeline CI/CD ;
- **Environment Variables** sur Render.

Secrets utilisés :

```text
DATABASE_URL
RENDER_DEPLOY_HOOK_URL
```

---

## Workflow Git

Le projet suit une organisation simple basée sur trois types de branches.

### `main`

Branche stable destinée aux versions validées.

### `develop`

Branche principale de développement.

### `feature/*`

Branches dédiées aux fonctionnalités.

Exemples :

```text
feature/api-model
feature/tests
feature/database
feature/ci-cd
feature/deploy
```

Les fonctionnalités sont développées indépendamment puis fusionnées dans `develop`.

---

## Conventions de commits

Exemples :

```text
feat: integrate trained XGBoost model into API
test: add API tests
feat: add PostgreSQL persistence for predictions
ci: add GitHub Actions test workflow
ci: add automatic Render deployment
docs: finalize project documentation
```

---

## Gestion des versions

Les versions stables du projet sont identifiées avec des tags Git.

Exemple :

```bash
git tag -a v1.0.0 -m "First production-ready POC"
git push origin v1.0.0
```

---

## Sécurité

Le projet est un POC et ne prétend pas couvrir toutes les exigences d’une API de production.

Mesures déjà présentes :

- validation stricte des entrées avec Pydantic ;
- secrets absents du dépôt Git ;
- connexion PostgreSQL via variable d’environnement ;
- HTTPS fourni par Render ;
- tests automatisés avant déploiement.

Améliorations possibles pour une version production :

- authentification par clé API ;
- OAuth2 ;
- rate limiting ;
- gestion de rôles ;
- monitoring ;
- logs structurés ;
- alerting ;
- rotation des secrets.

---

## Résultat

Le projet fournit un POC complet permettant :

1. d’envoyer les caractéristiques d’un employé à une API ;
2. de valider les données reçues ;
3. de transformer les données avec le préprocesseur du modèle ;
4. d’obtenir une prédiction XGBoost ;
5. d’enregistrer la prédiction dans PostgreSQL ;
6. de tester automatiquement l’application ;
7. de construire et déployer l’application avec Docker et GitHub Actions.

---

## Auteur

**Paul Larribet**
