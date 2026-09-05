from pydantic import BaseModel


class PredictionInput(BaseModel):
    feature_1: float
    feature_2: float


class PredictionOutput(BaseModel):
    prediction: int