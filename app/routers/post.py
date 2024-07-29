from fastapi import APIRouter,status,Depends,Response

from app.database import get_db
from .. import schema,models
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/posts",
    tags=["posts"]

)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post:schema.PostCreate,db: Session=Depends(get_db)):

    created_post=models.Post(**post.dict())
    # normally we use the post.dict() to note write all the field but its deprecated so i use the model_dump() that do the same 
    db.add(created_post)
    db.commit()

    return created_post