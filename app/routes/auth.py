from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserLogin
from app.auth import hash_password, verify_password, create_access_token
from app.users_db import users_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends



router = APIRouter(prefix="", tags=["Auth"])

@router.post("/signup")
def signup(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.email] = hash_password(user.password)
    return {"message": "User created successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    hashed = users_db.get(form_data.username)

    if not hashed or not verify_password(form_data.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": form_data.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
