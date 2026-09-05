from fastapi import FastAPI

from p5.model import predict_employee
from p5.schemas import PredictionInput, PredictionOutput
from p5.database import save_prediction

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

    input_data = data.model_dump()

    prediction, probability = predict_employee(
        input_data
    )

    save_prediction(
        input_data=input_data,
        prediction=prediction,
        probability=probability
    )

    return {
        "prediction": prediction,
        "probability": probability
    }