from fastapi import FastAPI
import psycopg

from . import models

from .database import engine,get_db

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# get_db()

# Dependency
# @app.get("/dbtest")
# async def root():
#     with psycopg.connect("dbname=batchdemo user=postgres password=admin") as conn:

# #  database="batchdemo",
# #      user="postgres",
# #      password="admin",
# #      host="localhost",
# #      port="5432", 
#         with conn.cursor() as cur:
#             cur.execute(

#             """
#                 CREATE TABLE rachid (
#                 id serial PRIMARY KEY,
#                 num integer,
#                 data text)
#             """
#         )

#         conn.commit()


#     return {"message": "tested db"}

@app.get("/")
async def root():
    return {"message": "Hello World"}