from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(filename, risk_score, severity, recommendation):
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    title_style = styles["Title"]

    doc = SimpleDocTemplate(filename)
    elements = []

    elements.append(Paragraph("Predictive Maintenance Report", title_style))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Risk Score: {risk_score}", style))
    elements.append(Paragraph(f"Severity: {severity}", style))
    elements.append(Paragraph(f"Recommendation: {recommendation}", style))

    doc.build(elements)