import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/machine_data.csv")

# ---------------- ADD REQUIRED COLUMNS ----------------
if "maintenance_history" not in df.columns:
    df["maintenance_history"] = 2

if "error_count" not in df.columns:
    df["error_count"] = 1

if "machine_type_Motor" not in df.columns:
    df["machine_type_Motor"] = 1

if "machine_type_Pump" not in df.columns:
    df["machine_type_Pump"] = 0

# ---------------- CREATE TARGET ----------------
if "failure" not in df.columns:
    df["failure"] = (
        (df["temperature"] > 90)
        | (df["vibration"] > 0.5)
        | (df["pressure"] > 60)
        | (df["runtime_hours"] > 300)
    ).astype(int)

# ---------------- EXACT FEATURES ----------------
FEATURE_COLUMNS = [
    "temperature",
    "vibration",
    "pressure",
    "runtime_hours",
    "maintenance_history",
    "error_count",
    "machine_type_Motor",
    "machine_type_Pump"
]

X = df[FEATURE_COLUMNS]
y = df["failure"]

# ---------------- TRAIN ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print(f"Model Accuracy: {acc * 100:.2f}%")

# ---------------- SAVE ----------------
joblib.dump(model, "models/predictive_model.pkl")
print("✅ NEW model saved successfully")