from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import models.category
import models.profile
import models.user
from schemas import category_create,category_out
from database import get_db
from utils import hash_password
from .oauth2 import verify_access_token


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=category_out.CategoryOut, status_code=201)
def create_category(category: category_create.CategoryCreate,  user_token = Depends(verify_access_token), db: Session = Depends(get_db)):
    is_category_exist = db.query(models.category.Category).filter(models.category.Category.name == category.name).first()
    if is_category_exist: 
         raise HTTPException(status_code=400, detail="Category with same name already exists !")
    new_category = models.category.Category(name=category.name, 
                                        slug=category.slug, 
                                        description=category.description, 
                                        image_url=category.image_url, 
                                        meta_title=category.meta_title, 
                                        meta_description=category.meta_description)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


