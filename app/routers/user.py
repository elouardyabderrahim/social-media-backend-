from fastapi import APIRouter, HTTPException,status,Depends,Response

from app.database import get_db
from .. import schema,models,utils
from sqlalchemy.orm import Session

from typing import List

router=APIRouter(
    prefix="/users",
    tags=["users"]

)


@router.get("/{user_id}",response_model=schema.UserOut)
async def get_user(user_id:int,db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.Post.id==user_id).first()
    

    if  not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with the id {user_id} not found")
    
    return user



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_post(user:schema.UserCreate,db: Session=Depends(get_db)):

     # hash the password - user.password
    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

