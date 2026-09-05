import json

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from p5.config import settings


engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def save_prediction(
    input_data: dict,
    prediction: int,
    probability: float
):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO predictions (
                    input_data,
                    prediction,
                    probability
                )
                VALUES (
                    CAST(:input_data AS JSONB),
                    :prediction,
                    :probability
                )
            """),
            {
                "input_data": json.dumps(input_data),
                "prediction": prediction,
                "probability": probability,
            }
        )