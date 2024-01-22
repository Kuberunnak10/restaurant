from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from src.restaurant_api.models import Dish
from src.restaurant_api.schemas import ResponseDishSchema, DishSchema

dish_router = APIRouter()


@dish_router.get('/{menu_id}/submenus/{submenu_id}/dishes')
def get_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    dishes = db.query(Dish).filter(Dish.submenu_id == submenu_id)
    if dishes is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dishes not found")
    dishes_list = [{"id": str(dish.id),
                    "title": dish.title,
                    'description': dish.description,
                    "price": dish.price} for dish in dishes]
    return dishes_list


@dish_router.get('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=ResponseDishSchema)
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

    dish_data = {"id": str(dish.id), "title": dish.title, "description": dish.description, "price": str(dish.price)}
    return dish_data


@dish_router.post('/{menu_id}/submenus/{submenu_id}/dishes', response_model=ResponseDishSchema,
                  status_code=status.HTTP_201_CREATED)
def create_dish(menu_id: int, submenu_id: int, item: DishSchema, db: Session = Depends(get_db)):
    dish = Dish(title=item.title, description=item.description, price=item.price, submenu_id=submenu_id)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    dish_data = {"id": str(dish.id),
                 "title": dish.title,
                 "description": dish.description,
                 "price": str(dish.price),
                 "submenu_id": submenu_id}
    return dish_data


@dish_router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=ResponseDishSchema)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, item: DishSchema, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    dish.title = item.title
    dish.description = item.description
    dish.price = item.price
    db.commit()
    db.refresh(dish)
    dish_data = {"id": str(dish.id), "title": dish.title, "description": dish.description, "price": str(dish.price)}
    return dish_data


@dish_router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', status_code=status.HTTP_200_OK)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    db.delete(dish)
    db.commit()
    dish_data = {"id": str(dish_id), "title": dish.title, "description": dish.description, 'price': str(dish.price)}
    return dish_data
