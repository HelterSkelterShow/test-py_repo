from pydantic import EmailStr, BaseModel

class CreateUser(BaseModel):
    email: EmailStr
