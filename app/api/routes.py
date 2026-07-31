from fastapi import APIRouter
from app.schemas.iris import IrisRequest, IrisResponse
from app.services.predictor import predict_species

router = APIRouter()

@router.post("/predict", response_model=IrisResponse)
def predict(data: IrisRequest):
    prediction = predict_species([
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ])

    return IrisResponse(prediction=prediction)