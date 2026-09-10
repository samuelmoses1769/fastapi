from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, Annotated,Literal
from datetime import datetime


# -------------------------
# Pydantic Model
# -------------------------

class Post(BaseModel):

    title: Annotated[
        str,
        Field(
            ...,
            description="Title of the post"
        )
    ]

    content: Annotated[
        str,
        Field(
            ...,
            description="Content of the post"
        )
    ]

    published: Annotated[
        bool,
        Field(
            ...,
            description="Whether the post is published"
        )
    ]


# -------------------------
# Update Model
# -------------------------

class UpdatePost(BaseModel):

    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


# -------------------------
# Response Model
# -------------------------

class PostResponse(Post):

    id: Annotated[
        int,
        Field(
            ...,
            description="Unique id for record"
        )
    ]

    timestamp: Annotated[
        datetime,
        Field(
            ...,
            description="Time at which record is created"
        )
    ]
    owner_id:Annotated[
        int,
        Field(
            ...,
            description="id of user who created the post"
        )
    ]
    owner:UserResponse
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            ...,
            description="Email of the person"
        )
    ]

    password: Annotated[
        str,
        Field(
            ...,
            description="Password for the account"
        )
    ]



class UserResponse(BaseModel):

    

    id: Annotated[
        int,
        Field(
            ...,
            description="Unique id for record"
        )
    ]
    email: EmailStr
    password:str
    timestamp: Annotated[
        datetime,
        Field(
            ...,
            description="Time at which record is created"
        )
    ]
    
    model_config = ConfigDict(from_attributes=True)

class PostOutput(BaseModel):
    Post:PostResponse
    vote:int
    model_config = ConfigDict(from_attributes=True)

class Vote(BaseModel):
    post_id:int
    dir:Literal[0,1]
