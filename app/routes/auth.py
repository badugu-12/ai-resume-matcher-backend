from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserLogin
from app.auth import hash_password, verify_password, create_access_token
from app.users_db import users_db

router = APIRouter(prefix="", tags=["Auth"])

@router.post("/signup")
def signup(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.email] = hash_password(user.password)
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin):
    hashed = users_db.get(user.email)
    if not hashed or not verify_password(user.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
