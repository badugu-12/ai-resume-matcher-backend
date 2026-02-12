from fastapi import APIRouter, UploadFile, File, Form, Depends, Header, HTTPException
from fastapi.responses import FileResponse
from app.utils.pdf_generator import generate_pdf
from app.auth import verify_token
import shutil

router = APIRouter(prefix="", tags=["PDF"])


# ✅ Manual Bearer Token Verification
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    email = verify_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return email


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
