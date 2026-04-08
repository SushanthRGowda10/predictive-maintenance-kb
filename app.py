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

# ✅ MUST match trained model exactly
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

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Model Info")
st.sidebar.write("Algorithm: Random Forest Classifier")
st.sidebar.write("Dataset: machine_data.csv")

st.sidebar.subheader("Features Used")
for feature in FEATURE_COLUMNS:
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
    humidity = st.number_input("Humidity", value=60.0)
    maintenance_history = st.number_input("Maintenance History", value=2)
    error_count = st.number_input("Error Count", value=1)

# ---------------- USER PREDICTION ----------------
if st.button("Predict Failure Risk"):
    risk_score = min(
        (
            temperature * 0.2
            + vibration * 100 * 0.3
            + pressure * 0.15
            + runtime_hours / 20
            + humidity * 0.05
            + error_count * 8
        ),
        100
    )

    severity = get_severity(risk_score)

    # ✅ EXACT trained schema
    input_data = pd.DataFrame([[
        temperature,
        vibration,
        pressure,
        runtime_hours,
        maintenance_history,
        error_count,
        1,  # machine_type_Motor
        0   # machine_type_Pump
    ]], columns=FEATURE_COLUMNS)

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

machine_ids = [f"MCH-{i}" for i in range(1, 11)]
machine_types = np.random.choice(
    ["Motor", "Pump", "Compressor"],
    size=10
)

fleet_rows = []

for machine_id, machine_type in zip(machine_ids, machine_types):
    temp = np.random.uniform(75, 110)
    vib = np.random.uniform(0.2, 0.7)
    press = np.random.uniform(35, 70)
    runtime = np.random.randint(100, 500)
    hum = np.random.uniform(45, 80)
    err = np.random.randint(0, 4)

    risk_score = min(
        (
            temp * 0.2
            + vib * 100 * 0.3
            + press * 0.15
            + runtime / 20
            + hum * 0.05
            + err * 8
        ),
        100
    )

    severity = get_severity(risk_score)
    failure_probability = round(risk_score / 100, 2)

    estimated_cost = (
        err * 200
        + runtime * 2
        + risk_score * 10
    )

    downtime_hours = round(
        failure_probability * runtime / 20,
        2
    )

    fleet_rows.append({
        "Machine ID": machine_id,
        "Machine Type": machine_type,
        "Temperature": round(temp, 2),
        "Vibration": round(vib, 2),
        "Pressure": round(press, 2),
        "Runtime Hours": runtime,
        "Risk Score": round(risk_score, 2),
        "Failure Probability": failure_probability,
        "Estimated Cost": round(estimated_cost, 2),
        "Downtime Hours": downtime_hours,
        "Severity": severity,
        "Status": "Critical" if risk_score > 80 else "Healthy"
    })

fleet_df = pd.DataFrame(fleet_rows).sort_values(
    "Risk Score",
    ascending=False
)

# ---------------- KPI CARDS ----------------
k1, k2, k3 = st.columns(3)

k1.metric("💰 Total Maintenance Cost", f"${fleet_df['Estimated Cost'].sum():,.0f}")
k2.metric("⚠️ Average Fleet Risk", f"{fleet_df['Risk Score'].mean():.1f}")
k3.metric("⏱️ Total Downtime", f"{fleet_df['Downtime Hours'].sum():.1f} hrs")

# ---------------- TABLE ----------------
st.dataframe(fleet_df, use_container_width=True)

# ---------------- ALERTS ----------------
critical_df = fleet_df[fleet_df["Risk Score"] > 80]

st.subheader("🚨 Critical Machine Alerts")
st.error(f"{len(critical_df)} machines need immediate maintenance")

if not critical_df.empty:
    st.dataframe(critical_df, use_container_width=True)

# ---------------- CHARTS ----------------
st.subheader("📊 Fleet Risk Distribution")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(fleet_df["Risk Score"], bins=10)
ax.set_xlabel("Risk Score")
ax.set_ylabel("Machines")
st.pyplot(fig)

st.subheader("📉 Fleet Temperature Trend")
st.line_chart(fleet_df["Temperature"])