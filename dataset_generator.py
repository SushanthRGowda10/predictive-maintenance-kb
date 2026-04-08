import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)

# Number of rows for advanced major project
n_rows = 1000

# Generate realistic industrial sensor values
temperature = np.random.normal(85, 12, n_rows).clip(50, 120)
vibration = np.random.normal(0.4, 0.18, n_rows).clip(0.1, 1.0)
pressure = np.random.normal(50, 15, n_rows).clip(20, 90)
runtime_hours = np.random.normal(250, 120, n_rows).clip(20, 600)

# Additional advanced features
machine_type = np.random.choice(["Motor", "Pump", "Compressor"], n_rows)
maintenance_history = np.random.randint(0, 6, n_rows)
error_count = np.random.randint(0, 10, n_rows)

# Advanced failure logic
risk_score = (
    (temperature > 95).astype(int)
    + (vibration > 0.65).astype(int)
    + (pressure > 65).astype(int)
    + (runtime_hours > 350).astype(int)
    + (error_count > 5).astype(int)
)

failure = (risk_score >= 2).astype(int)

# Severity score
severity = np.select(
    [risk_score <= 1, risk_score == 2, risk_score >= 3],
    ["Low", "Medium", "High"],
    default="Low"
)

# Build dataframe
df = pd.DataFrame({
    "temperature": np.round(temperature, 2),
    "vibration": np.round(vibration, 2),
    "pressure": np.round(pressure, 2),
    "runtime_hours": np.round(runtime_hours, 2),
    "machine_type": machine_type,
    "maintenance_history": maintenance_history,
    "error_count": error_count,
    "failure": failure,
    "severity": severity
})

# Save dataset
# IMPORTANT: save inside your existing data folder
output_path = "data/machine_data_advanced.csv"
df.to_csv(output_path, index=False)

print(f"Advanced 1000-row dataset created successfully: {output_path}")
print(df.head())
