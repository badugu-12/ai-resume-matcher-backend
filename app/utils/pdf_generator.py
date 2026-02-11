from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import uuid
import datetime

def generate_pdf(data: dict):
    file_name = f"resume_report_{uuid.uuid4()}.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Resume Match Report")

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated: {datetime.datetime.now()}")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Match Score: {data.get('match_percentage')}%")

    ats = data.get("ats_score", {})
    y -= 25
    c.drawString(50, y, f"ATS Score: {ats.get('score', 'N/A')}/100")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Resume Feedback:")

    y -= 20
    c.setFont("Helvetica", 11)
    for item in data.get("resume_feedback", []):
        c.drawString(60, y, f"- {item['title']}: {item['message']}")
        y -= 15

    c.showPage()
    c.save()

    return file_name
