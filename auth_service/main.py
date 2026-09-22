from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
import jwt
from datetime import datetime, timedelta
from .database import SessionLocal, engine, Base, User

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finans Servisi - Auth", description="Kullanıcı Kayıt, Giriş ve JWT Yönetimi")

SECRET_KEY = "finans_mikroservis_gizli_anahtar_key"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreateSchema(BaseModel):
    username: str
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

# Python Dahili Güvenli Şifreleme (Sıfır Dış Bağımlılık)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ENDPOINT 1: Kayıt
@app.post("/api/v1/auth/register", summary="Yeni Kullanıcı Kaydı")
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış!")
    
    hashed_pwd = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Kullanıcı başarıyla oluşturuldu", "user_id": new_user.id, "username": new_user.username}

# ENDPOINT 2: Giriş ve JWT Token
@app.post("/api/v1/auth/login", summary="Kullanıcı Girişi")
def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hatalı kullanıcı adı veya şifre!"
        )
    
    access_token = create_access_token(data={"sub": db_user.username, "user_id": db_user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Giriş başarılı"
    }