from decimal import Decimal

from pydantic import BaseModel


class DishSchema(BaseModel):
    title: str
    description: str
    price: Decimal

    class Config:
        orm_mode = True


class ResponseDishSchema(BaseModel):
    id: str
    title: str
    description: str
    price: str


class SubMenuSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class ResponseSubMenuSchema(BaseModel):
    title: str
    description: str
    id: str


class CountSubMenuResponse(ResponseSubMenuSchema):
    dishes_count: int


class MenuSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class ResponseMenuSchema(BaseModel):
    title: str
    description: str
    id: str


class CountMenuResponse(ResponseMenuSchema):
    submenus_count: int
    dishes_count: int
