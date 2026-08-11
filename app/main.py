from fastapi import FastAPI
from app.api.routes import router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="Secure MLOps Platform",
    version="1.0.0"
)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():
    return {"message": "Welcome to Secure MLOps Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(router)