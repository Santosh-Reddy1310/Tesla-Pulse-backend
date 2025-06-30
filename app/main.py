# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import stock_data, compare_data, chat  # 👈 include chat

app = FastAPI()

# 🌐 Allow CORS (so frontend can call API from browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_data.router)
app.include_router(compare_data.router)
app.include_router(chat.router)  # 👈 include chat router

@app.get("/")
def root():
    return {"message": "TeslaPulse API is running."}
