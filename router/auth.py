from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import models

import hash
import oauth
from fastapi.security import OAuth2PasswordRequestForm


router=APIRouter(tags=['auth'])


@router.post("/login")
def login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

    user_post=db.query(models.Users).filter(models.Users.email==user.username).first()

    if not user_post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials username")
    if not hash.verify_password(user.password,user_post.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials password")
    

    token=oauth.create_token(data={"user_id":user_post.id})

  
    return {"access_token": token, "token_type": "bearer"}
