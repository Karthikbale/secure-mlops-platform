from fastapi import FastAPI

app = FastAPI(
    title="Secure MLOps Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Secure MLOps Platform"
    }
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }