from sqlalchemy.sql import ddl
from sqlalchemy.sql.expression import delete
from fastapi import FastAPI, Depends, status, Response
from . import schemas, model
from .database import SessionLocal, engine
from sqlalchemy.orm import Session


app = FastAPI()

model.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}')
def destroy(id, db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).filter(
        model.Blog.id == id)
    if not blogs.first():
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available"}
    blogs.delete()
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).filter(model.Blog.id == id)
    if not blogs.first():
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available"}

    blogs.update({'title': request.title, 'body': request.body})

    db.commit()
    return 'updated'


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200)
def show(id, response: Response, db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blogs:
        # raise HTTPExecption(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Blog with the id {id} is not available")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available"}
    return blogs


@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = model.User(
        name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
