from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import UploadFile
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME="your_email@gmail.com",
    MAIL_PASSWORD="your_app_password",
    MAIL_FROM="your_email@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_report_email(email: str, pdf_bytes: bytes):
    message = MessageSchema(
        subject="Your AI Resume Matcher Report",
        recipients=[email],
        body="Your resume match report is attached.",
        attachments=[
            {
                "file": pdf_bytes,
                "filename": "resume_report.pdf",
                "content_type": "application/pdf",
            }
        ],
        subtype="plain",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
