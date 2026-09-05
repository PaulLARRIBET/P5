from fastapi import FastAPI


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