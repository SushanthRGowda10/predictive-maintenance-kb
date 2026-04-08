import os
import pandas as pd
from sklearn.ensemble import IsolationForest

# ---------------- DATA PATH ----------------
possible_paths = [
    "live_sensor_feed.csv",
    "data/machine_data.csv"
]

data_path = None
for path in possible_paths:
    if os.path.exists(path):
        data_path = path
        break

if data_path is None:
    raise FileNotFoundError("No dataset found for anomaly detection")

print(f"✅ Using dataset: {data_path}")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(data_path)

feature_cols = ["temperature", "vibration", "pressure", "runtime_hours"]
X = df[feature_cols]

# ---------------- ANOMALY MODEL ----------------
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df["anomaly_flag"] = model.fit_predict(X)

# Convert -1 => anomaly, 1 => normal
df["anomaly_status"] = df["anomaly_flag"].map({
    -1: "Anomaly",
    1: "Normal"
})

anomalies = df[df["anomaly_status"] == "Anomaly"]

print("\n🚨 Detected Anomalies")
print(anomalies.head())

df.to_csv("anomaly_results.csv", index=False)
print("\n✅ Saved anomaly_results.csv")