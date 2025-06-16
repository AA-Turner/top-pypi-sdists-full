from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel, EmailStr
from app.utils import hash_password, verify_password, create_access_token
from app.dependencies import get_db_hub, DatabaseHub, get_current_user  

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db_hub: DatabaseHub = Depends(get_db_hub)):
    await db_hub.connect_sqlite()
    async with db_hub.sqlite_conn.execute("SELECT * FROM users WHERE email = ?", (user.email,)) as cursor:
        existing = await cursor.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    await db_hub.sqlite_conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (user.email, hashed_pw))
    await db_hub.sqlite_conn.commit()

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db_hub: DatabaseHub = Depends(get_db_hub)):
    await db_hub.connect_sqlite()

    async with db_hub.sqlite_conn.execute("SELECT email, password FROM users WHERE email = ?", (form_data.username,)) as cursor:
        row = await cursor.fetchone()
        if not row or not verify_password(form_data.password, row[1]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": form_data.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}



@router.get("/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user
