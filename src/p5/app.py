from fastapi import FastAPI

from p5.schemas import PredictionInput, PredictionOutput


app = FastAPI(
    title="Futurisys ML API",
    description="API permettant d'exposer un modèle de machine learning",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Futurisys ML API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    prediction = 1 if data.feature_1 + data.feature_2 > 0 else 0

    return {"prediction": prediction}