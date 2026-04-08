def get_severity(temperature, vibration, pressure, runtime_hours, error_count):
    score = 0

    if temperature > 95:
        score += 2
    elif temperature > 85:
        score += 1

    if vibration > 0.6:
        score += 2
    elif vibration > 0.4:
        score += 1

    if pressure > 60:
        score += 2
    elif pressure > 45:
        score += 1

    if runtime_hours > 400:
        score += 2
    elif runtime_hours > 250:
        score += 1

    if error_count > 5:
        score += 2
    elif error_count > 2:
        score += 1

    if score >= 8:
        return "Critical"
    elif score >= 5:
        return "Medium"
    return "Low"


def get_solution(prediction, severity):
    if prediction == 1:
        if severity == "Critical":
            return (
                "Immediate shutdown required. "
                "Inspect motor bearings, lubrication system, "
                "cooling unit, and pressure valves."
            )
        elif severity == "Medium":
            return (
                "Schedule maintenance within 24 hours. "
                "Check vibration alignment, sensor calibration, "
                "and runtime load balancing."
            )
        else:
            return (
                "Routine preventive maintenance recommended. "
                "Monitor machine closely for the next cycle."
            )

    return "Machine healthy. Continue standard maintenance schedule."