from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.pdf_generator.generate_pdf import generate_pdf

import shutil
import os
import logging
from datetime import datetime

from app.parser.resume_parser import (
    extract_pdf_text,
    extract_email,
    extract_name,
    extract_skills,
    extract_education
)

from app.jd.jd_parser import (
    extract_jd_skills,
    extract_experience,
    extract_qualification
)

from app.matcher.matcher import compare_skills
from app.gap_analyzer.gap_analyzer import analyze_gaps
from app.feedback.feedback_agent import generate_feedback
from app.decision.decision_agent import make_decision
from app.ats.ats_score import calculate_ats_score


app = FastAPI(
    title="AI Resume Analyzer",
    description="Resume Screening using FastAPI",
    version="1.0"
)

# ---------------------------------
# Create Required Folders
# ---------------------------------

UPLOAD_FOLDER = "uploads"
LOG_FOLDER = "logs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# ---------------------------------
# Templates & Static Files
# ---------------------------------

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# ---------------------------------
# Logger
# ---------------------------------

last_report_filename = None

logger = logging.getLogger("resume_analyzer")
logger.setLevel(logging.INFO)

if not logger.handlers:

    file_handler = logging.FileHandler(
        os.path.join(LOG_FOLDER, "app.log"),
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# ---------------------------------
# Home Page
# ---------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
   
        "index.html",
        {
            "request": request
        }
    )

# ---------------------------------
# Resume Analyzer
# ---------------------------------

@app.post(
    "/analyze",
    response_class=HTMLResponse,
    summary="Analyze Resume",
    description="Upload a Resume PDF and compare it with the Job Description."
)
async def analyze_resume(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Validate PDF

    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    logger.info(f"Resume uploaded : {resume.filename}")

    file_path = os.path.join(
        UPLOAD_FOLDER,
        resume.filename
    )

    try:

        # Save Uploaded Resume

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                resume.file,
                buffer
            )

        # Extract Resume Text

        resume_text = extract_pdf_text(file_path)

        # Resume Details

        candidate_name = extract_name(file_path)
        candidate_email = extract_email(resume_text)
        education = extract_education(resume_text)
        resume_skills = extract_skills(resume_text)

        # Job Description Details

        jd_skills = extract_jd_skills(job_description)
        experience = extract_experience(job_description)
        qualification = extract_qualification(job_description)

        # Skill Matching

        match_result = compare_skills(
            resume_skills,
            jd_skills
        )

        # ATS Score

        ats_score = calculate_ats_score(
            match_result["match_percentage"]
        )

        # Gap Analysis

        gap_result = analyze_gaps(
            match_result["missing_skills"]
        )

        # Feedback

        feedback = generate_feedback(
            gap_result
        )

        # Decision

        decision = make_decision(
            match_result["match_percentage"]
        )

        logger.info(
            f"{candidate_name} analyzed successfully | ATS Score : {ats_score}%"
        )
                # Generate PDF Report
        report_data = {
            "candidate_name": candidate_name,
            "candidate_email": candidate_email,
            "education": education,

            "required_qualification": qualification,
            "required_experience": experience,

            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],

            "match_percentage": match_result["match_percentage"],
            "ats_score": ats_score,

            "feedback": feedback,

            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "reason": decision["reason"]
        }

        report_path = generate_pdf(report_data)
        report_filename = os.path.basename(report_path)
        global last_report_filename
        last_report_filename = report_filename


        # Return HTML Result Page

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,

                "candidate_name": candidate_name,
                "candidate_email": candidate_email,
                "education": education,

                "required_qualification": qualification,
                "required_experience": experience,

                "resume_skills": resume_skills,
                "required_skills": jd_skills,

                "matched_skills": match_result["matched_skills"],
                "missing_skills": match_result["missing_skills"],

                "match_percentage": match_result["match_percentage"],
                "ats_score": ats_score,

                "gap_analysis": gap_result,
                "feedback": feedback,

                "decision": decision["decision"],
                "confidence": decision["confidence"],
                "reason": decision["reason"],
                "pdf_available": True,
                "report_filename": report_filename
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume : {str(e)}"
        )

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/download-report")
async def download_report():

    global last_report_filename
    if not last_report_filename:
        raise HTTPException(
            status_code=404,
            detail="PDF report not found."
        )

    pdf_path = os.path.join("reports", last_report_filename)

    if os.path.exists(pdf_path):
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=last_report_filename
        )

    raise HTTPException(
        status_code=404,
        detail="PDF report not found."
    )