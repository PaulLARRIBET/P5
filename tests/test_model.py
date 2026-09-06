import pandas as pd
import pytest

from p5.model import add_features, predict_employee


def test_add_features():
    data = pd.DataFrame([{
        "annees_dans_le_poste_actuel": 2,
        "annees_dans_l_entreprise": 4,
        "annees_depuis_la_derniere_promotion": 1,
        "annes_sous_responsable_actuel": 2,
        "revenu_mensuel": 4000,
        "annee_experience_totale": 8,
        "nombre_experiences_precedentes": 2
    }])

    result = add_features(data)

    assert result["ratio_poste_entreprise"].iloc[0] == 0.5
    assert result["ratio_promotion_entreprise"].iloc[0] == 0.25
    assert result["ratio_manager_entreprise"].iloc[0] == 0.5
    assert result["revenu_par_experience"].iloc[0] == 500
    assert result["mobilite_carriere"].iloc[0] == 0.25


def test_add_features_zero_division():
    data = pd.DataFrame([{
        "annees_dans_le_poste_actuel": 0,
        "annees_dans_l_entreprise": 0,
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 0,
        "revenu_mensuel": 3000,
        "annee_experience_totale": 0,
        "nombre_experiences_precedentes": 0
    }])

    result = add_features(data)

    assert result["ratio_poste_entreprise"].iloc[0] == 0
    assert result["ratio_promotion_entreprise"].iloc[0] == 0
    assert result["ratio_manager_entreprise"].iloc[0] == 0
    assert result["revenu_par_experience"].iloc[0] == 0
    assert result["mobilite_carriere"].iloc[0] == 0


def test_prediction_known_case():
    data = {
        "genre": "F",
        "statut_marital": "Marié(e)",
        "departement": "Ressources Humaines",
        "poste": "Représentant Commercial",
        "heure_supplementaires": "Non",
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Aucun",
        "age": 24,
        "revenu_mensuel": 2033,
        "nombre_experiences_precedentes": 1,
        "annee_experience_totale": 1,
        "annees_dans_l_entreprise": 1,
        "annees_dans_le_poste_actuel": 0,
        "satisfaction_employee_environnement": 4,
        "note_evaluation_precedente": 3,
        "niveau_hierarchique_poste": 1,
        "satisfaction_employee_nature_travail": 2,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 3,
        "augementation_salaire_precedente": 13,
        "nombre_participation_pee": 1,
        "nb_formations_suivies": 2,
        "distance_domicile_travail": 13,
        "niveau_education": 2,
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 0
    }

    prediction, probability = predict_employee(data)

    assert prediction == 1
    assert probability == pytest.approx(
        0.35875294,
        rel=1e-5
    )