from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schema
import hash
import oauth

router = APIRouter(tags=["users"], prefix="/users")

@router.get("/", response_model=List[schema.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(oauth.get_current_user),
):
    return db.query(models.Users).all()



@router.get("/{id}", response_model=schema.UserResponse)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth.get_current_user),
):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user




@router.post(
    "/create",
    response_model=schema.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(record: schema.User, db: Session = Depends(get_db)):
    record.password = hash.hash_password(record.password)
    new_user = models.Users(**record.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user










