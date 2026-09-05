from fastapi import FastAPI

from p5.model import predict_employee
from p5.schemas import PredictionInput, PredictionOutput


app = FastAPI(
    title="Futurisys ML API",
    description="API permettant de prédire le départ d'un employé",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Futurisys ML API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post(
    "/predict",
    response_model=PredictionOutput
)
def predict(data: PredictionInput):

    prediction, probability = predict_employee(
        data.model_dump()
    )

    return {
        "prediction": prediction,
        "probability": probability
    }