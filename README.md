# Futurisys ML API

## Présentation

Ce projet est un Proof of Concept réalisé dans le cadre d’un projet OpenClassrooms.

L’objectif est de rendre un modèle de machine learning opérationnel et accessible via une API, tout en mettant en place les principales bonnes pratiques d’ingénierie logicielle :

- exposition d’un modèle de machine learning via FastAPI ;
- validation des données avec Pydantic ;
- tests automatisés avec Pytest ;
- stockage des prédictions dans PostgreSQL ;
- gestion du code avec Git et GitHub ;
- conteneurisation avec Docker ;
- intégration continue avec GitHub Actions ;
- déploiement automatique sur Render.

Le modèle utilisé est un classifieur XGBoost permettant de prédire le départ potentiel d’un employé.

## Architecture du projet

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

## Technologies utilisées

- Python 3.12
- FastAPI
- Pydantic
- XGBoost
- Scikit-learn
- Pandas
- PostgreSQL
- SQLAlchemy
- Pytest
- pytest-cov
- Docker
- Git
- GitHub
- GitHub Actions
- Render
- uv

## Installation locale

Cloner le dépôt :

git clone https://github.com/PaulLARRIBET/P5.git
cd P5

Installer les dépendances :

uv sync

Activer l’environnement virtuel :

source .venv/bin/activate

## Variables d’environnement

Créer un fichier .env à la racine du projet.

Exemple :

DATABASE_URL=postgresql://paullarribet@localhost:5432/p5

Le fichier .env n’est pas versionné afin de protéger les informations sensibles.

## Base de données PostgreSQL

Le projet utilise PostgreSQL pour enregistrer les prédictions réalisées par l’API.

La table est créée à partir du script :

sql/create_tables.sql

Structure principale :

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_data JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    probability DOUBLE PRECISION NOT NULL
);

Chaque prédiction enregistre :

- les données d’entrée ;
- la classe prédite ;
- la probabilité associée ;
- la date de création.

## Lancer l’API en local

Depuis la racine du projet :

uv run uvicorn p5.app:app --app-dir src --reload

L’API est disponible sur :

http://127.0.0.1:8000

Documentation Swagger :

http://127.0.0.1:8000/docs

## Endpoints

### GET /

Permet de vérifier que l’API répond.

Exemple :

{
  "message": "Futurisys ML API is running"
}

### GET /health

Endpoint de contrôle de l’état de l’application.

Exemple :

{
  "status": "ok"
}

### POST /predict

Permet d’obtenir une prédiction du modèle à partir des caractéristiques d’un employé.

Exemple de réponse :

{
  "prediction": 1,
  "probability": 0.587685227394104
}

## Modèle de machine learning

Le modèle est un XGBClassifier entraîné préalablement.

Deux fichiers sont utilisés :

models/best_xgb.pkl
models/preprocessor.pkl

Le premier contient le modèle entraîné.

Le second contient le preprocessor Scikit-learn utilisé pour transformer les données avant prédiction.

Le preprocessor est ajusté uniquement sur les données d’entraînement puis réutilisé avec transform() lors de l’inférence.

## Feature engineering

Certaines variables sont créées automatiquement avant la prédiction :

- ratio_poste_entreprise
- ratio_promotion_entreprise
- ratio_manager_entreprise
- revenu_par_experience
- mobilite_carriere

Ces variables sont recréées dans l’API avant l’application du preprocessor.

## Validation des données

Pydantic est utilisé pour valider les données envoyées à l’API.

Les variables catégorielles sont limitées aux valeurs autorisées.

Exemple :

genre: Literal["F", "M"]

Les variables numériques disposent également de contraintes.

Exemple :

age: int = Field(ge=0, le=100)

Une requête invalide retourne automatiquement une erreur HTTP 422.

## Tests

Les tests sont écrits avec Pytest.

Ils couvrent notamment :

- l’endpoint /health ;
- une prédiction valide ;
- les erreurs de validation ;
- les valeurs catégorielles invalides ;
- les valeurs numériques hors limites.

Pour lancer les tests :

PYTHONPATH=src uv run pytest tests -v

## Couverture des tests

Pour générer le rapport de couverture :

PYTHONPATH=src uv run pytest --cov=src/p5 --cov-report=term-missing

Couverture obtenue lors du développement :

97 %

## Docker

Construire l’image :

docker build -t p5-api .

Lancer le conteneur :

docker run --rm \
  -p 7860:7860 \
  -e DATABASE_URL="postgresql://user:password@host:5432/p5" \
  p5-api

L’API est alors disponible sur :

http://127.0.0.1:7860

## Déploiement

L’application est déployée sur Render.

URL publique :

https://p5-tqd4.onrender.com

Documentation Swagger :

https://p5-tqd4.onrender.com/docs

La base PostgreSQL de production est également hébergée sur Render.

La variable DATABASE_URL est stockée dans les variables d’environnement Render et n’est pas présente dans le code source.

## CI/CD

Le pipeline CI/CD est configuré avec GitHub Actions dans :

.github/workflows/ci.yml

Le pipeline réalise les étapes suivantes :

push / pull request
        ↓
installation de Python
        ↓
installation des dépendances
        ↓
création d'une base PostgreSQL de test
        ↓
création des tables
        ↓
exécution des tests Pytest
        ↓
si les tests réussissent
        ↓
déploiement automatique sur Render

Le déploiement est déclenché uniquement après validation des tests.

## Gestion des secrets

Les informations sensibles ne sont jamais enregistrées dans le dépôt Git.

Les secrets sont gérés via :

- les variables d’environnement locales ;
- GitHub Secrets ;
- les variables d’environnement Render.

Exemples :

DATABASE_URL
RENDER_DEPLOY_HOOK_URL

## Gestion Git

Le projet utilise plusieurs types de branches :

main
develop
feature/*

main contient les versions stables.

develop contient la version en cours de développement.

Les branches feature/* sont utilisées pour développer les différentes fonctionnalités.

Exemples :

feature/api-model
feature/tests
feature/database
feature/ci-cd
feature/deploy

## Conventions de commits

Exemples :

feat: integrate trained XGBoost model into API
test: add API tests
feat: add PostgreSQL persistence for predictions
ci: add GitHub Actions test workflow
ci: add automatic Render deployment

## Gestion des versions

Les versions stables peuvent être identifiées avec des tags Git.

Exemple :

git tag -a v1.0.0 -m "First production-ready POC"
git push origin v1.0.0

## Sécurité

Le projet est un Proof of Concept.

Les mesures mises en place incluent :

- validation stricte des entrées avec Pydantic ;
- gestion des secrets hors du dépôt Git ;
- accès à PostgreSQL via variable d’environnement ;
- déploiement HTTPS sur Render.

Dans une version de production complète, des mécanismes supplémentaires pourraient être ajoutés :

- authentification par clé API ;
- OAuth2 ;
- rate limiting ;
- journalisation renforcée ;
- contrôle des rôles et permissions.

## Auteur

Paul Larribet