import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ---------------- SIMULATION SETTINGS ----------------
rows = 100
start_time = datetime.now()

runtime_hours = np.arange(1, rows + 1)
temperature = np.random.normal(85, 5, rows)
vibration = np.random.normal(60, 7, rows)
pressure = np.random.normal(30, 4, rows)

# ---------------- ADD ANOMALY SPIKES ----------------
for i in [20, 45, 70, 90]:
    temperature[i] += 20
    vibration[i] += 25
    pressure[i] += 10

# ---------------- BUILD DATAFRAME ----------------
df = pd.DataFrame({
    "timestamp": [start_time + timedelta(minutes=i) for i in range(rows)],
    "runtime_hours": runtime_hours,
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure
})

df.to_csv("live_sensor_feed.csv", index=False)

print("✅ live_sensor_feed.csv generated successfully")
print(df.head())