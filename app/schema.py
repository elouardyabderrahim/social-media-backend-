# pydantic for the types validation
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode=True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None