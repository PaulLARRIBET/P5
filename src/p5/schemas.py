from typing import Literal

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):

    # Variables catégorielles
    genre: Literal["F", "M"]

    statut_marital: Literal[
        "Célibataire",
        "Divorcé(e)",
        "Marié(e)"
    ]

    departement: Literal[
        "Consulting",
        "Commercial",
        "Ressources Humaines"
    ]
    poste: Literal[
        "Cadre Commercial",
        "Assistant de Direction",
        "Consultant",
        "Tech Lead",
        "Manager",
        "Senior Manager",
        "Représentant Commercial",
        "Directeur Technique",
        "Ressources Humaines"
    ]

    heure_supplementaires: Literal[
        "Non",
        "Oui"
    ]

    domaine_etude: Literal[
        "Infra & Cloud",
        "Transformation Digitale",
        "Marketing",
        "Entrepreunariat",
        "Autre",
        "Ressources Humaines"
    ]

    frequence_deplacement: Literal[
        "Aucun",
        "Occasionnel",
        "Frequent"
    ]

    # Variables numériques
    age: int = Field(
        ge=0,
        le=100,
        description="Âge de l'employé"
    )

    revenu_mensuel: int = Field(
        ge=0,
        description="Revenu mensuel de l'employé"
    )

    nombre_experiences_precedentes: int = Field(
        ge=0
    )

    annee_experience_totale: int = Field(
        ge=0
    )

    annees_dans_l_entreprise: int = Field(
        ge=0
    )

    annees_dans_le_poste_actuel: int = Field(
        ge=0
    )

    satisfaction_employee_environnement: int = Field(
        ge=1,
        le=5
    )

    note_evaluation_precedente: int = Field(
        ge=1,
        le = 5
    )

    niveau_hierarchique_poste: int = Field(
        ge=1,
        le = 5
    )

    satisfaction_employee_nature_travail: int = Field(
        ge=1,
        le=5
    )

    satisfaction_employee_equipe: int = Field(
        ge=1,
        le=5
    )

    satisfaction_employee_equilibre_pro_perso: int = Field(
        ge=1,
        le=5
    )

    note_evaluation_actuelle: int = Field(
        ge=1,
        le = 5
    )

    augementation_salaire_precedente: float = Field(
        ge=0
    )

    nombre_participation_pee: int = Field(
        ge=0
    )

    nb_formations_suivies: int = Field(
        ge=0
    )

    distance_domicile_travail: int = Field(
        ge=0
    )

    niveau_education: int = Field(
        ge=1,
        le = 5
    )

    annees_depuis_la_derniere_promotion: int = Field(
        ge=0
    )

    annes_sous_responsable_actuel: int = Field(
        ge=0
    )


class PredictionOutput(BaseModel):
    prediction: int
    probability: float = Field(
        ge=0,
        le=1
    )