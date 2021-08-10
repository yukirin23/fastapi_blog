from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import schemas, model, database, oath2
from sqlalchemy.orm import Session
from .. repository import blog


router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)

get_db = database.get_db


@router.get('/')
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.create(request, db)


@router.delete('/{id}')
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.update(id, request, db)


@router.get('/{id}', status_code=200)
def show(id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.show(id, db)
