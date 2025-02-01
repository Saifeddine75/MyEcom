from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models.user
import database, schemas, models, utils
from . import oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_cerd: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.user.User).filter(models.user.User.email == user_cerd.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not utils.verify(user_cerd.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token" : access_token, "token_type": "bearer"}