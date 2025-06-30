# backend/app/model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

from stock_data import fetch_tesla_data

# 🚀 Step 1: Load Tesla stock data
df = fetch_tesla_data()

# 🧹 Step 2: Clean + Create Features & Target
# We'll predict tomorrow's "close" using today's data

df["close_next"] = df["close"].shift(-1)  # next day's close
df.dropna(inplace=True)  # Drop last row which has no "next close"

X = df[["open", "high", "low", "volume"]]  # Features
y = df["close_next"]  # Target

# 🎯 Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🧠 Step 4: Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# 📊 Step 5: Evaluate Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"🧪 Model Mean Squared Error: {mse:.2f}")

# 💾 Step 6: Save Model
model_dir = "../model"
os.makedirs(model_dir, exist_ok=True)
joblib.dump(model, os.path.join(model_dir, "stock_model.pkl"))
print("✅ Model saved to model/stock_model.pkl")
