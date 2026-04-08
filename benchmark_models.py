import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# ---------------- ROBUST DATA PATH ----------------
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
    raise FileNotFoundError(
        "No dataset found. Checked: data/machine_data_adv.csv, data/machine_data.csv"
    )

print(f"✅ Using dataset: {data_path}")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(data_path)

TARGET_COLUMN = "failure"

if TARGET_COLUMN not in df.columns:
    raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataset")

X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODELS ----------------
models = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC()
}

results = []

# ---------------- BENCHMARK ----------------
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": round(accuracy_score(y_test, preds), 4),
        "Precision": round(precision_score(y_test, preds), 4),
        "Recall": round(recall_score(y_test, preds), 4),
        "F1 Score": round(f1_score(y_test, preds), 4)
    })

results_df = pd.DataFrame(results).sort_values("F1 Score", ascending=False)

print("\n📊 Benchmark Results")
print(results_df)

results_df.to_csv("benchmark_results.csv", index=False)
print("\n✅ benchmark_results.csv saved successfully")