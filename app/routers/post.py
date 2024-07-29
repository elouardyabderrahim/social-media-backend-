from fastapi import APIRouter, HTTPException,status,Depends,Response

from app.database import get_db
from .. import schema,models
from sqlalchemy.orm import Session

from typing import List, Optional

router=APIRouter(
    prefix="/posts",
    tags=["posts"]

)


@router.get("/",response_model=List[schema.Post])
async def get_all_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(models.Post).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching posts")


@router.get("/{post_id}",response_model=schema.Post)
async def get_post(post_id:int,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==post_id)

    
    if  not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with the id {post_id} not found")
    
    return post
    
    
    
   

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post:schema.PostCreate,db: Session=Depends(get_db)):

    created_post=models.Post(**post.dict())
    # normally we use the post.dict() to note write all the field but its deprecated so i use the model_dump() that do the same 
    db.add(created_post)
    db.commit()

    return created_post


@router.patch("/{post_id}",response_model=schema.Post)
def patch_post(post_id:int,post_updated:schema.PostUpdate,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==post_id).first()

    if  not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with the id {post_id} not found")
    
    fields_to_update=post_updated.dict(exclude_unset=True)  # Get only the fields that were set in the request
    
    for key, value in fields_to_update.items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post) # database to refresh column-oriented attributes with the current value available in the current transaction.
    
    
    return post
    


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    """
    synchronize_session=False:

    This is an argument specific to SQLAlchemy's update method. It controls whether the session
    should be synchronized with the changes made by the update statement.
    When set to False, it means that SQLAlchemy does not need to synchronize 
    the session state with the database changes. This is typically used for performance reasons, especially when you are making bulk updates.
    
    """

    db.commit()

    return post_query.first()


@router.delete("/{id_post}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_post: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id_post)

    print(post_query)
    if post_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {str(id)} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    # db.refresh()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)