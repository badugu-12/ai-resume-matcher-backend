# Utility functions
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_match_pdf(data: dict) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "AI Resume Matcher Report")

    c.setFont("Helvetica", 11)
    c.drawString(50, 770, f"Match Score: {data['match_percentage']}%")
    c.drawString(50, 750, f"ATS Score: {data['ats_score']['score']}/100")

    y = 720
    c.drawString(50, y, "Resume Suggestions:")
    y -= 20

    for item in data.get("resume_feedback", []):
        c.drawString(60, y, f"- {item['title']}")
        y -= 15
        c.drawString(70, y, item["message"])
        y -= 20

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

