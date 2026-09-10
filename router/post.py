from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func
from schema import Post, UpdatePost
from database import get_db
import models
import schema
import oauth


router = APIRouter(tags=["posts"], prefix="/posts")

@router.get("/", response_model=List[schema.PostOutput])
def posts(
    db: Session = Depends(get_db),
    current_user= Depends(oauth.get_current_user),
    search:Optional[str]=""
):

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
        .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .all()
    )

    return results

    

    


# # -------------------------
# # READ ONE
# # GET /records/{pid}
# # -------------------------

@router.get("/{pid}", response_model=schema.PostOutput)
def post_record(
    pid: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth.get_current_user),
):

    post = ( db.query(models.Post, func.count(models.Vote.post_id).label("vote"))
            .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)
    
            .group_by(models.Post.id)
            .filter(models.Post.id == pid).first())

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post ID not found"
        )
    if post.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorized to requested opeartion ")
    

    return post


# # -------------------------
# # CREATE
# # POST /create
# # -------------------------

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.PostResponse
)
def create_record(
    post: Post,
    db: Session = Depends(get_db),
    current_user = Depends(oauth.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


  

    

    


# # -------------------------
# # UPDATE
# # PUT /update/{pid}
# # -------------------------
@router.put("/update/{pid}")
def update_record(
    pid: int,
    post: UpdatePost,
    db: Session = Depends(get_db),
    current_user = Depends(oauth.get_current_user),
):
    # Find the record
    post_query = db.query(models.Post).filter(
        models.Post.id == pid
    )
    post=post_query.first()
    # Check if ID exists
    if post  is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post ID not found"
        )

    # Get only fields that were provided
    update_data = post.model_dump(exclude_unset=True)

    # Check if nothing was provided
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update"
        )

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorizec to update the post")

    # Update the database
    post_query.update(
        update_data,
        synchronize_session=False
    )

    # Save changes
    db.commit()

    return {"msg": "Successful"}

# # # -------------------------
# # # DELETE
# # # DELETE /delete/{pid}
# # # -------------------------
@router.delete("/delete/{pid}", response_model=schema.PostResponse)
def delete_record(
    pid: int,
    db: Session = Depends(get_db),
    current_user= Depends(oauth.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == pid).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post ID not found"
        )

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorizec to delete the post")

    deleted_post = post

    db.delete(post)
    db.commit()

    return deleted_post
