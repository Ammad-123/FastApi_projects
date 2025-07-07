from fastapi import APIRouter, HTTPException, Depends
from schemas import UserIn, UserOut, Token
from database import fake_users_db, get_user
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"]) 

@router.post("/signup", response_model=UserOut)  # /auth/signup
def signup(user: UserIn):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "password": hashed}
    return {"username": user.username}

@router.post("/login", response_model=Token) # auth/login
def login(user: UserIn):
    db_user = get_user(user.username)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}




