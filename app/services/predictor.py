import joblib
from fastapi import HTTPException

MODEL_PATH = "app/models/model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Model not found at {MODEL_PATH}")

label_map = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}

def predict_species(features):
    try:
        prediction = model.predict([features])[0]
        return label_map[int(prediction)]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )