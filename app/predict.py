# backend/app/predict.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/predict/tesla")
def predict_tsla():
    # 🔮 Dummy prediction value
    return {
        "prediction": "up",
        "confidence": 0.91
    }
