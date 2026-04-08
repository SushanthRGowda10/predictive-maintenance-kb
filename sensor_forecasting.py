import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# ---------------- DATA PATH ----------------
possible_paths = [
    "data/machine_data_adv.csv",
    "data/machine_data.csv",
    "machine_data_adv.csv",
    "machine_data.csv"
]

data_path = None
for path in possible_paths:
    if os.path.exists(path):
        data_path = path
        break

if data_path is None:
    raise FileNotFoundError("Dataset not found")

print(f"✅ Using dataset: {data_path}")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(data_path)

if "runtime_hours" not in df.columns or "temperature" not in df.columns:
    raise ValueError("Required columns not found")

# ---------------- TRAIN SIMPLE FORECAST MODEL ----------------
X = df[["runtime_hours"]]
y = df["temperature"]

model = LinearRegression()
model.fit(X, y)

# ---------------- FUTURE FORECAST ----------------
future_hours = np.arange(
    df["runtime_hours"].max() + 1,
    df["runtime_hours"].max() + 25
).reshape(-1, 1)

future_temp = model.predict(future_hours)

forecast_df = pd.DataFrame({
    "future_runtime_hours": future_hours.flatten(),
    "predicted_temperature": future_temp
})

print("\n📈 Next 24-Hour Forecast")
print(forecast_df.head())

forecast_df.to_csv("temperature_forecast.csv", index=False)

# ---------------- PLOT ----------------
plt.figure(figsize=(10, 6))
plt.plot(forecast_df["future_runtime_hours"], forecast_df["predicted_temperature"])
plt.xlabel("Future Runtime Hours")
plt.ylabel("Predicted Temperature")
plt.title("Next 24-Hour Temperature Forecast")
plt.tight_layout()
plt.savefig("temperature_forecast.png")

print("\n✅ Saved: temperature_forecast.csv and temperature_forecast.png")