from typing import Annotated
from fastapi import Path, APIRouter

from src.items.schemas import CreateUser

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.post("/")
def get_name(user: CreateUser, name: str = "world"):
    name = name.title()
    return {
        "name":f"hello, {name}",
        "email":user.email
    }

@router.post("/email/{id}")
def set_email(user: CreateUser, id :Annotated[int, Path(ge=1,lt=1000000)]):
    return {
        "message" : "success",
        "id":id,
        "email": user.email
    }