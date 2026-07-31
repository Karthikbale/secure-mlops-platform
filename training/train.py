from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# Train model
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Create models directory if it doesn't exist
os.makedirs("app/models", exist_ok=True)

# Save model
joblib.dump(model, "app/models/model.pkl")

print("Model trained successfully!")
print("Model saved to app/models/model.pkl")