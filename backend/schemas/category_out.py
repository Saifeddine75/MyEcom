from pydantic import BaseModel

class CategoryOut(BaseModel):
    name: str
    description: str
    slug: str
    image_url: str