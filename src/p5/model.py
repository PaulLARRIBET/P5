import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import json


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "best_xgb.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"
CONFIG_PATH = BASE_DIR / "models" / "model_config.json"


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(PREPROCESSOR_PATH, "rb") as f:
    preprocessor = pickle.load(f)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    model_config = json.load(f)

THRESHOLD = float(model_config["threshold"])


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ratio_poste_entreprise"] = (
        df["annees_dans_le_poste_actuel"]
        / df["annees_dans_l_entreprise"].replace(0, np.nan)
    )

    df["ratio_promotion_entreprise"] = (
        df["annees_depuis_la_derniere_promotion"]
        / df["annees_dans_l_entreprise"].replace(0, np.nan)
    )

    df["ratio_manager_entreprise"] = (
        df["annes_sous_responsable_actuel"]
        / df["annees_dans_l_entreprise"].replace(0, np.nan)
    )

    df["revenu_par_experience"] = (
        df["revenu_mensuel"]
        / df["annee_experience_totale"].replace(0, np.nan)
    )

    df["mobilite_carriere"] = (
        df["nombre_experiences_precedentes"]
        / df["annee_experience_totale"].replace(0, np.nan)
    )

    new_features = [
        "ratio_poste_entreprise",
        "ratio_promotion_entreprise",
        "ratio_manager_entreprise",
        "revenu_par_experience",
        "mobilite_carriere",
    ]

    df[new_features] = df[new_features].fillna(0)

    return df


def predict_employee(data: dict):
    df = pd.DataFrame([data])

    df = add_features(df)

    X = preprocessor.transform(df)

    probability = float(model.predict_proba(X)[0, 1])
    prediction = int(probability >= THRESHOLD)

    return prediction, probability