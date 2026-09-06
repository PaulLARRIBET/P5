# Futurisys ML API

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-pytest-success.svg)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](https://www.docker.com/)
[![Deploy](https://img.shields.io/badge/deploy-Render-46E3B7.svg)](https://render.com/)

## Présentation

Ce projet est un **Proof of Concept** réalisé dans le cadre d’un projet OpenClassrooms.

L’objectif est de rendre un modèle de machine learning opérationnel et accessible via une API, tout en appliquant des bonnes pratiques d’ingénierie logicielle et de déploiement :

- exposition du modèle via **FastAPI** ;
- validation des entrées avec **Pydantic** ;
- tests unitaires et fonctionnels avec **Pytest** ;
- stockage du dataset et des prédictions dans **PostgreSQL** ;
- gestion du code avec **Git / GitHub** ;
- conteneurisation avec **Docker** ;
- intégration et déploiement continus avec **GitHub Actions** ;
- déploiement cloud sur **Render**.

Le modèle utilisé est un **XGBoost Classifier** permettant de prédire le départ potentiel d’un employé.

---

## Architecture du projet

```text
P5/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── employees.csv
├── docs/
│   └── database_schema.png
├── models/
│   ├── best_xgb.pkl
│   ├── preprocessor.pkl
│   └── model_config.json
├── scripts/
│   └── import_dataset.py
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
│   ├── test_api.py
│   └── test_model.py
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
| Données | Pandas / NumPy |
| Base de données | PostgreSQL |
| Accès base | SQLAlchemy |
| Tests | Pytest / pytest-cov |
| Conteneurisation | Docker |
| Versioning | Git / GitHub |
| CI/CD | GitHub Actions |
| Hébergement | Render |
| Dépendances | uv |

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

Le fichier `.env` est ignoré par Git afin de ne pas exposer d’informations sensibles.

Un fichier `.env.example` est fourni comme modèle.

---

## Base de données PostgreSQL

Le projet utilise PostgreSQL pour :

- stocker le dataset historique complet ;
- conserver la traçabilité des appels au modèle ;
- enregistrer les inputs, outputs, probabilités et dates de prédiction.

Deux tables principales sont utilisées.

### Table `employees`

Cette table contient le dataset historique utilisé pour le projet ML.

Elle contient les variables métier brutes ainsi que la cible `a_quitte_l_entreprise`.

### Table `predictions`

```sql
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_data JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    probability DOUBLE PRECISION NOT NULL
);
```

Chaque appel à `/predict` enregistre :

- les données d’entrée ;
- la classe prédite ;
- la probabilité associée ;
- la date de création.

### Création des tables

Le schéma SQL est défini dans :

```text
sql/create_tables.sql
```

Pour créer les tables dans PostgreSQL :

```bash
psql p5
```

Puis dans `psql` :

```sql
\i /chemin/vers/P5/sql/create_tables.sql
```

### Import du dataset

Le dataset complet est stocké dans :

```text
data/employees.csv
```

L’import dans PostgreSQL est réalisé avec :

```bash
PYTHONPATH=src uv run python scripts/import_dataset.py
```

---

## Schéma de la base de données

Le schéma UML de la base est disponible dans :

```text
docs/database_schema.png
```

![Schéma UML de la base de données](docs/database_schema.png)

La table `employees` contient le dataset historique complet.

La table `predictions` assure la traçabilité des appels à l’API. Les inputs sont stockés en JSONB afin de conserver la requête complète sans imposer de relation artificielle avec le dataset historique.

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

Endpoint de contrôle de l’état de l’application.

Exemple :

```json
{
  "status": "ok"
}
```

### `POST /predict`

Retourne une prédiction du modèle et la probabilité associée.

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

Trois fichiers sont chargés par l’API :

```text
models/best_xgb.pkl
models/preprocessor.pkl
models/model_config.json
```

- `best_xgb.pkl` contient le modèle entraîné ;
- `preprocessor.pkl` contient le préprocesseur Scikit-learn ajusté sur les données d’entraînement ;
- `model_config.json` contient les paramètres d’inférence, notamment le seuil de décision.

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

## Seuil de décision

Le modèle retourne une probabilité de départ de l’employé.

Le seuil de classification retenu est :

```text
0.062
```

La règle de décision est donc :

```text
probability >= 0.062  → prediction = 1
probability < 0.062   → prediction = 0
```

Ce seuil a été sélectionné afin d’obtenir un meilleur compromis entre le rappel et l’accuracy que le seuil standard de `0.5`.

Le seuil est stocké dans :

```text
models/model_config.json
```

Exemple :

```json
{
  "threshold": 0.062
}
```

Cette séparation permet de modifier le seuil d’inférence sans modifier directement le code de l’API.

---

## Performances du modèle

Le modèle a été évalué avec plusieurs métriques de classification :

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Le seuil optimal a été recherché afin d’obtenir un compromis adapté entre la capacité à détecter les départs et la performance globale du modèle.

Les métriques finales sont issues du notebook d’entraînement et doivent rester cohérentes avec la version de `best_xgb.pkl` déployée.

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

### Tests API

Ils couvrent notamment :

- l’endpoint `/` ;
- l’endpoint `/health` ;
- une prédiction valide ;
- une catégorie invalide ;
- une valeur numérique hors limites.

### Tests du modèle

Ils couvrent notamment :

- le feature engineering ;
- les divisions par zéro ;
- un cas fonctionnel réel issu du dataset ;
- la cohérence entre probabilité et prédiction.

Lancer tous les tests :

```bash
PYTHONPATH=src uv run pytest -v
```

---

## Couverture de tests

Générer le rapport :

```bash
PYTHONPATH=src uv run pytest --cov=src/p5 --cov-report=term-missing
```

Couverture obtenue lors du développement :

```text
95 %
```

---

## Choix techniques

### FastAPI

FastAPI a été retenu car il permet :

- de créer rapidement une API REST ;
- de bénéficier d’une documentation Swagger/OpenAPI automatique ;
- d’intégrer naturellement Pydantic ;
- de disposer d’un framework léger et adapté au déploiement de modèles ML.

### Pydantic

Pydantic valide les données avant leur passage au modèle et évite les entrées incohérentes ou incompatibles.

### PostgreSQL

PostgreSQL est utilisé pour :

- stocker le dataset historique ;
- enregistrer chaque appel au modèle ;
- assurer la traçabilité des inputs et outputs.

### SQLAlchemy

SQLAlchemy centralise les interactions Python/PostgreSQL et simplifie la gestion de la connexion.

### Docker

Docker garantit un environnement reproductible entre le développement local et le déploiement cloud.

### GitHub Actions

GitHub Actions automatise :

- l’installation des dépendances ;
- le démarrage d’un PostgreSQL de test ;
- la création des tables ;
- l’exécution de Pytest ;
- la validation avant fusion ;
- le déclenchement du déploiement.

### Render

Render a été retenu comme plateforme cloud équivalente à Hugging Face Spaces, adaptée au déploiement d’une API FastAPI conteneurisée avec Docker et à l’hébergement PostgreSQL.

---

## Environnements

### Développement

Exécution locale avec :

- FastAPI ;
- PostgreSQL local ;
- fichier `.env` ;
- Docker pour valider l’image de production.

### Test

GitHub Actions crée un environnement temporaire avec :

- Python ;
- les dépendances du projet ;
- PostgreSQL de test ;
- les tables nécessaires ;
- Pytest.

### Production

L’API est déployée sur Render via Docker.

La base PostgreSQL de production est également hébergée sur Render.

Les secrets sont stockés dans les variables d’environnement de la plateforme.

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

L’API est disponible sur :

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
test: add model unit and functional tests
feat: add PostgreSQL persistence for predictions
feat: add employee dataset and database documentation
feat: apply optimized prediction threshold
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

## Maintenance et mise à jour du modèle

Le modèle peut être mis à jour sans modifier l’architecture générale de l’API.

### Mise à jour

1. Réentraîner le modèle dans le projet ML.
2. Sélectionner la meilleure version du modèle.
3. Exporter le nouveau modèle dans `models/best_xgb.pkl`.
4. Exporter le préprocesseur associé dans `models/preprocessor.pkl`.
5. Mettre à jour le seuil dans `models/model_config.json`.
6. Remplacer les anciens artefacts dans le dossier `models/`.

### Validation

Lancer les tests :

```bash
PYTHONPATH=src uv run pytest -v
```

Puis la couverture :

```bash
PYTHONPATH=src uv run pytest --cov=src/p5 --cov-report=term-missing
```

Une Pull Request doit ensuite être créée vers `develop`.

Le pipeline GitHub Actions valide automatiquement les tests avant fusion.

### Déploiement

Après validation et merge sur `develop` :

```text
GitHub Actions
→ tests
→ validation
→ Render Deploy Hook
→ nouvelle version déployée
```

---

## Sécurité

Le projet est un POC.

Les mesures déjà présentes incluent :

- validation stricte des entrées avec Pydantic ;
- secrets absents du dépôt Git ;
- connexion PostgreSQL via variable d’environnement ;
- HTTPS fourni par Render ;
- tests automatisés avant déploiement.

Améliorations possibles pour une version de production :

- authentification par clé API ;
- OAuth2 ;
- rate limiting ;
- contrôle des rôles ;
- monitoring ;
- logs structurés ;
- alerting ;
- rotation des secrets.

---

## Limites du POC

Pour une utilisation à plus grande échelle, plusieurs améliorations pourraient être ajoutées :

- monitoring des performances du modèle ;
- détection de data drift ;
- détection de model drift ;
- versionnement avancé des modèles ;
- stratégie de rollback ;
- authentification renforcée ;
- gestion de la montée en charge ;
- suivi des temps de réponse et erreurs.

Les performances du modèle doivent être réévaluées régulièrement afin de déterminer si un réentraînement est nécessaire.

---

## Résultat

Le projet fournit un POC complet permettant :

1. d’envoyer les caractéristiques d’un employé à une API ;
2. de valider les données reçues ;
3. de recréer les features nécessaires ;
4. de transformer les données avec le préprocesseur entraîné ;
5. de calculer une probabilité avec XGBoost ;
6. d’appliquer un seuil de décision optimisé ;
7. d’enregistrer les inputs et outputs dans PostgreSQL ;
8. de tester automatiquement l’application ;
9. de déployer automatiquement l’API via Docker, GitHub Actions et Render.

---

## Auteur

**Paul Larribet**
