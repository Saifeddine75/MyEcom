from pydantic import BaseModel, Field
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(None, example="Smartphones")
    description: str = Field(None, example="Smartphones category")
    parent_category_id: int = Field(None, example="1")
    slug: Optional[str]
    image_url:  Optional[str]
    is_active: bool = Field(None, example=True)
    meta_title: Optional[str] = Field(None, example="Custom Title for SEO")
    meta_description: Optional[str] = Field(None, example="Custom Description for SEO")