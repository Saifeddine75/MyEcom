from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class ProfileCreate(BaseModel):
    phone_number: Optional[str] = Field(None, example="+33612345678")
    country: Optional[str] = Field(None, example="France")
    postal_address: Optional[str] = Field(None, example="75001 Paris")

    # ✅ Utilisation d'un validateur Pydantic
    @field_validator("phone_number")
    @classmethod
    def check_phone_number(cls, value: str) -> str:
        pattern = r"^\+?[1-9]\d{1,14}$"
        if not re.match(pattern, value):
            raise ValueError("Numéro de téléphone invalide. Format attendu: +123456789")
        return value