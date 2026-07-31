import joblib

MODEL_PATH = "app/models/model.pkl"

model = joblib.load(MODEL_PATH)

label_map = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}

def predict_species(features):
    prediction = model.predict([features])[0]
    return label_map[int(prediction)]