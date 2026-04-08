def get_severity(risk_score):
    if risk_score >= 85:
        return "Critical"
    elif risk_score >= 65:
        return "High"
    elif risk_score >= 40:
        return "Medium"
    else:
        return "Low"


def get_solution(risk_score):
    if risk_score >= 85:
        return (
            "🚨 Immediate shutdown recommended. "
            "Perform full inspection and emergency maintenance."
        )
    elif risk_score >= 65:
        return (
            "⚠️ High risk detected. "
            "Schedule preventive maintenance within 24 hours."
        )
    elif risk_score >= 40:
        return (
            "🛠️ Moderate risk. "
            "Monitor machine closely and service this week."
        )
    else:
        return (
            "✅ Machine healthy. Continue regular monitoring."
        )