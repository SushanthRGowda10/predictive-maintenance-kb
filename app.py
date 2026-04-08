import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from knowledge_base import get_solution, get_severity
from report_generator import generate_report

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Predictive Maintenance Knowledge Base",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
MODEL_PATH = "models/predictive_model.pkl"
model = joblib.load(MODEL_PATH)

# ✅ Read exact trained schema dynamically
MODEL_FEATURES = list(model.feature_names_in_)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Model Info")
st.sidebar.write("Algorithm: Random Forest Classifier")
st.sidebar.write("Loaded trained schema dynamically")

st.sidebar.subheader("Features Used")
for feature in MODEL_FEATURES:
    st.sidebar.write(f"• {feature}")

# ---------------- TITLE ----------------
st.title("🛠️ Predictive Maintenance Knowledge Base")
st.subheader("AI-Driven Predictive Maintenance and Fleet BI Dashboard")

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("Temperature", value=85.0)
    vibration = st.number_input("Vibration", value=0.35)
    pressure = st.number_input("Pressure", value=40.0)
    runtime_hours = st.number_input("Runtime Hours", value=200.0)

with col2:
    maintenance_history = st.number_input("Maintenance History", value=2)
    error_count = st.number_input("Error Count", value=1)
    machine_type = st.selectbox("Machine Type", ["Motor", "Pump"])

# ---------------- USER PREDICTION ----------------
if st.button("Predict Failure Risk"):
    risk_score = min(
        (
            temperature * 0.2
            + vibration * 100 * 0.3
            + pressure * 0.15
            + runtime_hours / 20
            + error_count * 8
        ),
        100
    )

    severity = get_severity(risk_score)

    # ✅ Create schema-safe row
    row = {feature: 0 for feature in MODEL_FEATURES}

    if "temperature" in row:
        row["temperature"] = temperature
    if "vibration" in row:
        row["vibration"] = vibration
    if "pressure" in row:
        row["pressure"] = pressure
    if "runtime_hours" in row:
        row["runtime_hours"] = runtime_hours
    if "maintenance_history" in row:
        row["maintenance_history"] = maintenance_history
    if "error_count" in row:
        row["error_count"] = error_count

    # handle one-hot safely
    motor_col = "machine_type_Motor"
    pump_col = "machine_type_Pump"

    if motor_col in row:
        row[motor_col] = 1 if machine_type == "Motor" else 0
    if pump_col in row:
        row[pump_col] = 1 if machine_type == "Pump" else 0

    input_data = pd.DataFrame([row])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("⚠️ Machine Failure Likely")
    else:
        st.success("✅ Machine Healthy")

    recommendation = get_solution(risk_score)

    st.warning(f"Severity Level: {severity}")
    st.info(recommendation)

    if st.button("Generate PDF Report"):
        generate_report(
            "maintenance_report.pdf",
            round(risk_score, 2),
            severity,
            recommendation
        )
        st.success("✅ PDF report generated successfully")

# ---------------- FLEET DASHBOARD ----------------
st.header("🏭 Industrial Fleet Monitoring Dashboard")

fleet_df = pd.DataFrame({
    "Machine ID": [f"MCH-{i}" for i in range(1, 11)],
    "Temperature": np.random.uniform(75, 110, 10),
    "Risk Score": np.random.uniform(20, 100, 10),
})

fleet_df["Severity"] = fleet_df["Risk Score"].apply(get_severity)
fleet_df["Failure Probability"] = (fleet_df["Risk Score"] / 100).round(2)
fleet_df["Estimated Cost"] = (fleet_df["Risk Score"] * 100).round(2)
fleet_df["Downtime Hours"] = (fleet_df["Failure Probability"] * 10).round(2)

# ---------------- KPI ----------------
k1, k2, k3 = st.columns(3)

k1.metric("💰 Total Maintenance Cost", f"${fleet_df['Estimated Cost'].sum():,.0f}")
k2.metric("⚠️ Average Fleet Risk", f"{fleet_df['Risk Score'].mean():.1f}")
k3.metric("⏱️ Total Downtime", f"{fleet_df['Downtime Hours'].sum():.1f} hrs")

# ---------------- TABLE ----------------
st.dataframe(fleet_df, use_container_width=True)

# ---------------- CHARTS ----------------
st.subheader("📊 Fleet Risk Distribution")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(fleet_df["Risk Score"], bins=10)
st.pyplot(fig)

st.subheader("📉 Fleet Temperature Trend")
st.line_chart(fleet_df["Temperature"])