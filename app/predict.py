from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PredictInput(BaseModel):
    open: float
    high: float
    low: float
    volume: float

@router.post("/predict")
def predict_price(data: PredictInput):
    # Replace this with ML model logic if available
    predicted = (data.open + data.high + data.low + data.volume) / 4
    return {"predicted_close": round(predicted, 2)}
