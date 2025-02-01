from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    email: EmailStr
    id: int

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # class Config:
    #     from_attributes = True
