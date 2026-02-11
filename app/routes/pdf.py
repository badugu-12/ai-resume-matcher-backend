from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from app.utils.pdf_generator import generate_pdf
from app.auth import verify_token
from fastapi.security import OAuth2PasswordBearer
import shutil

router = APIRouter(prefix="", tags=["PDF"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

@router.post("/download-report")
async def download_report(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: str = Depends(get_current_user)
):
    path = f"temp_{resume.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    pdf_path = generate_pdf(path, job_description, current_user)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="AI_Resume_Report.pdf"
    )
