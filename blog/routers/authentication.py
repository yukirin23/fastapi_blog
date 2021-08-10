from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import schemas, model, database, JWTtoken
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

get_db = database.get_db


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(
        model.User.email == request.username).first()
    if not user:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': "invalid credential"}

    if not Hash.verify(user.password, request.password):
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': "Incorrect password"}

    # generate a jwt token and return
    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTtoken.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
