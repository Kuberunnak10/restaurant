from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from src.restaurant_api.schemas import ResponseSubMenuSchema, SubMenuSchema, CountSubMenuResponse
from src.restaurant_api.models import Submenu, Dish
from src.database import get_db

submenu_router = APIRouter()


@submenu_router.get('/{menu_id}/submenus/')
def get_submenus(menu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id)
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    submenu_list = [{'id': str(submenu.id),
                     'title': submenu.title,
                     'description': submenu.description} for submenu in submenu]
    return submenu_list


@submenu_router.get('/{menu_id}/submenus/{submenu_id}', response_model=CountSubMenuResponse)
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id, ).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    dish_count = db.query(func.count(Dish.id)).filter(Dish.submenu_id == submenu.id).scalar()
    submenu_data = {'id': str(submenu.id),
                    'title': submenu.title,
                    'description': submenu.description,
                    'dishes_count': dish_count}

    return submenu_data


@submenu_router.post("/{menu_id}/submenus/", response_model=ResponseSubMenuSchema, status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: int, item: SubMenuSchema, db: Session = Depends(get_db)):
    submenu = Submenu(title=item.title, description=item.description, menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    submenu_data = {'id': str(submenu.id),
                    'title': submenu.title,
                    'description': submenu.description,
                    'menu_id': menu_id}
    return submenu_data


@submenu_router.patch("/{menu_id}/submenus/{submenu_id}", response_model=ResponseSubMenuSchema)
def update_submenu(menu_id: int, submenu_id: int, item: SubMenuSchema, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    submenu.title = item.title
    submenu.description = item.description
    db.commit()
    db.refresh(submenu)
    submenu_data = {'id': str(submenu.id),
                    'title': submenu.title,
                    'description': submenu.description}

    return submenu_data


@submenu_router.delete("/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    db.delete(submenu)
    db.commit()
    submenu_data = {'id': submenu.id,
                    'title': submenu.title,
                    'description': submenu.description}
    return submenu_data
