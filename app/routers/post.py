import logging
from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.database import get_db
from .. import schema, models
from sqlalchemy.orm import Session
from typing import List, Optional

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[schema.Post])
async def get_all_posts(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all posts")
        posts = db.query(models.Post).all()
        logger.debug(f"Retrieved {len(posts)} posts")
        return posts
    except Exception as e:
        logger.error(f"An error occurred while fetching posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching posts")

@router.get("/{post_id}", response_model=schema.Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching post with id {post_id}")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        logger.warning(f"Post with id {post_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id {post_id} was not found")
    
    logger.debug(f"Post with id {post_id} retrieved successfully")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    logger.info("Creating a new post")
    created_post = models.Post(**post.dict())
    # normally we use the post.dict() to note write all the field but its deprecated so i use the model_dump() that do the same 
    db.add(created_post)
    db.commit()
    logger.debug(f"Post with id {created_post.id} created successfully")
    return created_post

@router.patch("/{post_id}", response_model=schema.Post)
def patch_post(post_id: int, post_updated: schema.PostUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating post with id {post_id}")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        logger.warning(f"Post with id {post_id} not found for update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id {post_id} was not found")

    fields_to_update = post_updated.dict(exclude_unset=True)  # Get only the fields that were set in the request
    for key, value in fields_to_update.items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post)  # database to refresh column-oriented attributes with the current value available in the current transaction.
    
    logger.debug(f"Post with id {post_id} updated successfully")
    return post

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    logger.info(f"Updating post with id {id}")
# cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        logger.warning(f"Post with id {id} does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    """
    synchronize_session=False:

    This is an argument specific to SQLAlchemy's update method. It controls whether the session
    should be synchronized with the changes made by the update statement.
    When set to False, it means that SQLAlchemy does not need to synchronize 
    the session state with the database changes. This is typically used for performance reasons, especially when you are making bulk updates.
    """

    db.commit()
    logger.debug(f"Post with id {id} updated successfully")
    return post_query.first()

@router.delete("/{id_post}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_post: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting post with id {id_post}")
    post_query = db.query(models.Post).filter(models.Post.id == id_post)

    if post_query.first() is None:
        logger.warning(f"Post with id {id_post} does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id_post} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    # db.refresh()
    
    logger.debug(f"Post with id {id_post} deleted successfully")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
