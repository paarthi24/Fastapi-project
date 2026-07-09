from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def generate_pdf(data):

    output_folder = "reports"
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_name = "".join(
        c for c in data["candidate_name"] if c.isalnum() or c in (" ", "_", "-")
    ).strip().replace(" ", "_") or "Candidate"
    filename = f"Resume_Report_{sanitized_name}_{timestamp}.pdf"
    file_path = os.path.join(output_folder, filename)

    c = canvas.Canvas(file_path, pagesize=letter)

    y = 770

    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, y, "Resume Analysis Report")

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Candidate Name : {data['candidate_name']}")
    y -= 20

    c.drawString(50, y, f"Email : {data['candidate_email']}")
    y -= 20

    c.drawString(50, y, f"Education : {data['education']}")
    y -= 30

    c.drawString(50, y, f"Required Qualification : {data['required_qualification']}")
    y -= 20

    c.drawString(50, y, f"Required Experience : {data['required_experience']}")
    y -= 30

    c.drawString(50, y, f"ATS Score : {data['ats_score']}%")
    y -= 20

    c.drawString(50, y, f"Match Percentage : {data['match_percentage']}%")
    y -= 30

    c.drawString(50, y, "Matched Skills:")
    y -= 20

    for skill in data["matched_skills"]:
        c.drawString(70, y, f"• {skill}")
        y -= 18

    y -= 10

    c.drawString(50, y, "Missing Skills:")
    y -= 20

    for skill in data["missing_skills"]:
        c.drawString(70, y, f"• {skill}")
        y -= 18

    y -= 10

    c.drawString(50, y, "Feedback:")
    y -= 20

    for item in data["feedback"]:
        c.drawString(
            70,
            y,
            f"{item['skill']} : {item['suggestion']}"
        )
        y -= 18

    y -= 20

    c.drawString(50, y, f"Decision : {data['decision']}")
    y -= 20

    c.drawString(50, y, f"Confidence : {data['confidence']}")
    y -= 20

    c.drawString(50, y, f"Reason : {data['reason']}")

    c.save()

    return file_path