from fastapi import FastAPI


import logging

from app import models
from app.logs.logging_config import setup_logging

from .database import engine
from .routers import post ,user


setup_logging()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = logging.getLogger(__name__)


logger.info("info message.........")
app.include_router(post.router)
app.include_router(user.router)