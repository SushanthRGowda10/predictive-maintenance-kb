import json
from datetime import datetime

model_metadata = {
    "model_name": "Predictive Maintenance Random Forest",
    "model_version": "v2.0",
    "training_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "dataset_version": "machine_data.csv",
    "benchmark_best_model": "Random Forest",
    "benchmark_f1_score": 1.0,
    "forecasting_enabled": True,
    "iot_simulation_enabled": True,
    "deployment_status": "Ready"
}

with open("model_metadata.json", "w") as f:
    json.dump(model_metadata, f, indent=4)

print("✅ model_metadata.json created successfully")
print(model_metadata)