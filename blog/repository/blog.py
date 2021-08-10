from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import model, schemas


def get_all(db: Session):
    blogs = db.query(model.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db: Session):
    blogs = db.query(model.Blog).filter(
        model.Blog.id == id)
    if not blogs.first():
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available"}
    blogs.delete()
    db.commit()
    return 'done'


def update(id: int, request: schemas.Blog, db: Session):
    blogs = db.query(model.Blog).filter(model.Blog.id == id)
    if not blogs.first():
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available"}

    blogs.update({'title': request.title, 'body': request.body})

    db.commit()
    return 'updated'


def show(id: int, db: Session):
    blogs = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blogs:
        # raise HTTPExecption(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f"Blog with the id {id} is not available")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"Blog with the id {id} is not available"}
    return blogs
