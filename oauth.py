from datetime import datetime, timedelta, timezone
from fastapi import status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from  sqlalchemy.orm import Session
from database import get_db
from config import settings
import models
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_token(data: dict) -> str:
   
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token:str):
    try:
        payload=jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id=payload.get('user_id')
        if user_id is None:
            raise  credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
        
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    user_id = verify_token(token)          
    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()
