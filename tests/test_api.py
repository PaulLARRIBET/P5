from fastapi.testclient import TestClient

from p5.app import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Futurisys ML API is running"
    }

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_valid():
    payload = {
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

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1

def test_predict_invalid_genre():
    payload = {
        "genre": "X",
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

    response = client.post("/predict", json=payload)

    assert response.status_code == 422

def test_predict_invalid_age():
    payload = {
        "genre": "F",
        "statut_marital": "Célibataire",
        "departement": "Consulting",
        "poste": "Cadre Commercial",
        "heure_supplementaires": "Oui",
        "domaine_etude": "Infra & Cloud",
        "frequence_deplacement": "Aucun",
        "age": 150,
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

    response = client.post("/predict", json=payload)

    assert response.status_code == 422