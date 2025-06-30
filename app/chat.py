from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests

load_dotenv()

router = APIRouter()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message

    # 🔍 Fetch latest Tesla stock data
    url = f"https://api.twelvedata.com/time_series?symbol=TSLA&interval=1day&apikey={TWELVE_DATA_API_KEY}&outputsize=1"
    stock_response = requests.get(url)
    try:
        data = stock_response.json()["values"][0]
        open_price = data["open"]
        high_price = data["high"]
        low_price = data["low"]
        close_price = data["close"]
        stock_date = data["datetime"]
    except:
        return {"response": "Unable to fetch Tesla stock data right now."}

    # 🧠 Build contextual prompt for Gemini
    prompt = f"""
    You are a stock market assistant. Use the most recent Tesla (TSLA) data to respond.

    🧾 Tesla Stock Snapshot (latest available):
    Date: {stock_date}
    Open: ${open_price}
    High: ${high_price}
    Low: ${low_price}
    Close: ${close_price}

    Now answer this question based on the above data:
    {user_message}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return {"response": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}