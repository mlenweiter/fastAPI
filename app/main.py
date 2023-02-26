from random import randrange
from turtle import pos, title
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
import time
import utils.models as models
from utils.database import SessionLocal, engine
from sqlalchemy.orm import Session
from utils.database import get_db
from utils import schemas
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='martin', password='m',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successful')
        break
    except Exception as error:
        time.sleep(2)
        print(error)


@app.get(
    "/posts", response_model=List[schemas.Post])  # decorator: turns this function into an API endpoint; .get is the HTTP method that the API user should use
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = {kwarg}""".format(kwarg=str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="post with id: {kwarg} does not exitst".format(kwarg=id))

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = {kwarg} RETURNING *""".format(kwarg=id))
    # conn.commit()
    # deleted_post = cursor.fetchone()

    query = db.query(models.Post).filter(models.Post.id == id)


    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="post with id: {kwarg} does not exitst".format(kwargs=id))
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @app.put("/posts/{id}")
# def update_post(id: int, post: Post, db: Session = Depends(get_db)):
#     # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id= %s 
#     # RETURNING *;""", (post.title, post.content, post.published, str(id)))

#     # conn.commit()
#     # result = cursor.fetchone()

#     query = db.query(models.Post).filter(models.Post.id == id)


#     if query.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#         detail="post with id: {kwarg} does not exitst".format(kwarg=id))

    
#     new_post = query.update(post.dict(), synchronize_session=False)
#     db.commit()


#     return {"data": query.first()}
