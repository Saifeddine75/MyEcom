from pydantic import BaseModel

class ProfileOut(BaseModel):
    phone_number: str
    country: str
    postal_address: str