from pydantic import BaseModel
from typing import List, Optional


# Запросы на создание пользователя
class CreateUserRequest(BaseModel):
    username: str
    password: str

# Токены доступа
class Token(BaseModel):
    access_token: str
    token_type: str

class ICoverImage(BaseModel):
    image: str

class CartUpdate(BaseModel):
    quantity: int



class IProductItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    discount: float
    hit: Optional[bool] = None
    releaseDate: Optional[str] = None
    brand: str
    digital: bool
    categories: List[str]
    cover: str
    amount: int
    images: List[ICoverImage]
    reviews: Optional[List[str]] = None

    class Config:
        orm_mode = True
