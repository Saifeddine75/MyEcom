from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import models.profile
import models.user
from schemas import user_create, user_out, user_response, profile_create, profile_out
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

@router.post("/{id}/profile/", response_model=profile_out.ProfileOut, status_code=201)
def create_profile(id:int, profile: profile_create.ProfileCreate, user_token = Depends(verify_access_token), db: Session = Depends(get_db)):
    print(f"🔍 DEBUG: Token reçu dans l'endpoint: {user_token}")
    user = db.query(models.user.User).filter(models.user.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="No User Found")
    
    is_exist = db.query(models.profile.Profile).filter(models.profile.Profile.user_id == id).first()
    if is_exist:
        raise HTTPException(status_code=400, detail="Profile already exists : please try updating")
    
    new_profile = models.profile.Profile(phone_number=profile.phone_number,
                                         country=profile.country,
                                         postal_address=profile.postal_address,
                                         user_id = id
                                         )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile



@router.put("/{id}/profile/", response_model=profile_out.ProfileOut, status_code=201)
def create_profile(id:int, profile_update: profile_create.ProfileCreate, user_token = Depends(verify_access_token), db: Session = Depends(get_db)):
    print(f"🔍 DEBUG: Token reçu dans l'endpoint: {user_token}")
      # Vérifier si le profil existe
    profile = db.query(models.profile.Profile).filter(models.profile.Profile.user_id == id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profil non trouvé")

    # Mettre à jour les champs
    update_data = profile_update.dict(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile