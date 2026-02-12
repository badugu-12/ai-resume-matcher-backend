from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.match import router as match_router
from app.routes.pdf import router as pdf_router

app = FastAPI(title="AI Resume Job Matcher")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-resume-matcher-frontend-six.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 🔥 THIS IS THE KEY
app.include_router(auth_router)
app.include_router(match_router)
app.include_router(pdf_router)
