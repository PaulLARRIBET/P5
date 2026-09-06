from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from p5.config import settings


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "employees.csv"


def import_dataset():
    df = pd.read_csv(CSV_PATH)

    engine = create_engine(settings.database_url)

    df.to_sql(
        "employees",
        engine,
        if_exists="append",
        index=False
    )

    print(f"{len(df)} lignes importées dans la table employees.")


if __name__ == "__main__":
    import_dataset()