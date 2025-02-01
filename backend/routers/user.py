from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import models.user
from schemas import user_create, user_out, user_response
from database import get_db
from utils import hash_password
from .oauth2 import verify_access_token


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_out.UserOut, status_code=201)
def create_user(user: user_create.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = models.user.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model= user_response.UserResponse)
async def get_user( id: int, user_token = Depends(verify_access_token), db: Session = Depends(get_db)):
    print(f"🔍 DEBUG: Token reçu dans l'endpoint: {user_token}")
    user = db.query(models.user.User).filter(models.user.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")
    
    return user