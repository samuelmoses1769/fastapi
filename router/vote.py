from fastapi import APIRouter,HTTPException,status,Depends
from database import get_db
import oauth
import schema
import models
from sqlalchemy.orm import Session

router=APIRouter(tags=['Votes'],prefix="/votes")


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db:Session=Depends(get_db),current_user=Depends(oauth.get_current_user)):
    post_found=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id).first()
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    post=query.first()
    query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    post=query.first()
    if vote.dir==1:
        if post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"{vote.user_id} already liked the post")
        new_vote=models.Vote(user_id=current_user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"msg":"successfully voted"}
    else:
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not like found")
        
        else:
            query.delete(synchronize_session=False)
            db.commit()
            return {"msg":"successfully deleted vote"}