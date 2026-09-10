from database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False)
    timestamp = Column(TIMESTAMP, server_default=text("now()"))
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    owner=relationship("Users")



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    timestamp = Column(TIMESTAMP, server_default=text("now()"))

class Vote(Base):
    __tablename__="Votes"
    post_id = Column(
            Integer,
            ForeignKey("posts.id", ondelete="CASCADE"),
            nullable=False,
            primary_key=True
        )

    user_id = Column(
                Integer,
                ForeignKey("users.id", ondelete="CASCADE"),
                nullable=False,
                primary_key=True
            )
