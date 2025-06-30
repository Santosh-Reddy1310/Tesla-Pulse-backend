from fastapi import APIRouter
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")  # Or set your API key directly

@router.get("/compare")
def get_compare_data():
    symbols = ["TSLA", "RIVN", "LCID"]
    url = "https://api.twelvedata.com/time_series"
    params = {
        "interval": "1day",
        "apikey": TWELVE_DATA_API_KEY,
        "outputsize": 1
    }

    result = []

    for symbol in symbols:
        params["symbol"] = symbol
        response = requests.get(url, params=params)
        data = response.json()

        print(f"Fetched {symbol}: {data}")  # 🪵 Log the raw response

        if "values" in data:
            latest = data["values"][0]
            result.append({
                "symbol": symbol,
                "open": float(latest["open"]),
                "high": float(latest["high"]),
                "low": float(latest["low"]),
                "close": float(latest["close"]),
            })

    print("Final Compare Result:", result)  # 🪵 Log final result
    return result
