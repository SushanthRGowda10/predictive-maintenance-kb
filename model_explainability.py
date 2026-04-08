import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

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

TARGET_COLUMN = "failure"
X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

# ---------------- TRAIN MODEL ----------------
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# ---------------- FEATURE IMPORTANCE ----------------
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\n📊 Feature Importance")
print(importance_df)

importance_df.to_csv("feature_importance.csv", index=False)

# ---------------- PLOT ----------------
plt.figure(figsize=(10, 6))
plt.barh(importance_df["Feature"], importance_df["Importance"])
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Feature Importance - Predictive Maintenance")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("feature_importance.png")
print("\n✅ Saved: feature_importance.csv and feature_importance.png")