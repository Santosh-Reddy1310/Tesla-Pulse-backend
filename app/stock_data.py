# backend/app/stock_data.py

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from fastapi import APIRouter

router = APIRouter()

# 🔐 Load environment variables (like your API key from a .env file)
load_dotenv()
API_KEY = os.getenv("TWELVE_DATA_API_KEY")

# 🧠 Function to fetch Tesla stock data
def fetch_tesla_data(interval='1day', outputsize=30):
    url = f"https://api.twelvedata.com/time_series"
    
    params = {
        "symbol": "TSLA",  # Tesla stock symbol
        "interval": interval,  # Daily data
        "outputsize": outputsize,  # Number of data points (days)
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 🛑 Check for errors
    if "values" not in data:
        raise ValueError("Failed to fetch Tesla stock data: " + str(data.get("message", "Unknown error")))

    # 📊 Convert JSON to DataFrame
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    # 📉 Convert string numbers to floats
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.sort_values("datetime", inplace=True)

    return df

@router.get("/stock")
def get_stock_data():
    try:
        df = fetch_tesla_data()
        data = df.to_dict(orient="records")
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

