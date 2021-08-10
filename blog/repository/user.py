from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import model, schemas
from .. hashing import Hash


def create(request: schemas.User, db: Session):
    new_user = model.User(
        name=request.name, email=request.email, password=Hash.bcrypt_code(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(id: int, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        # raise HTTPExecption(status_code=status.HTTP_404_NOT_FOUND,
        #                    detail=f"User with the id {id} is not available")
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f"user with the id {id} is not available"}
    else:
        return user
