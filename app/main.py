from fastapi import FastAPI
import psycopg

from . import models

from .database import engine,get_db
from .routers import post ,user
app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(post.router)
app.include_router(user.router)