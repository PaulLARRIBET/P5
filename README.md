# Futurisys ML API

## Présentation

Ce projet a pour objectif de mettre en production un modèle de machine learning à travers une API.

Le Proof of Concept devra notamment permettre :

* d’exposer un modèle de machine learning via une API développée avec FastAPI ;
* de tester l’application avec Pytest ;
* de stocker des données dans une base PostgreSQL ;
* de mettre en place un pipeline CI/CD ;
* de gérer le projet avec Git et GitHub.

## Structure du projet

```text
P5/
├── src/        # Code source de l'application
├── tests/      # Tests unitaires et fonctionnels
├── scripts/    # Scripts utilitaires
├── sql/        # Scripts SQL
├── pyproject.toml
├── uv.lock
└── README.md
```

## Prérequis

* Python 3.12
* Git
* uv

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/PaulLARRIBET/P5.git
cd P5
```

Installer les dépendances :

```bash
uv sync
```

Activer l'environnement virtuel :

```bash
source .venv/bin/activate
```

## Gestion des branches

Le projet utilise les conventions suivantes :

* `main` : version stable du projet ;
* `develop` : branche principale de développement ;
* `feature/*` : développement des nouvelles fonctionnalités.

Exemples :

```text
feature/api
feature/model
feature/database
feature/tests
feature/ci-cd
```

## Gestion des versions

Les versions stables du projet seront identifiées à l'aide de tags Git.

Exemple :

```bash
git tag v1.0.0
```

## Auteur

Paul Larribet
