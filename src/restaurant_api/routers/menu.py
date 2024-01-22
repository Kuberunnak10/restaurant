from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from src.restaurant_api.models import Menu, Dish, Submenu
from src.restaurant_api.schemas import MenuSchema, ResponseMenuSchema, CountMenuResponse

menu_router = APIRouter()


@menu_router.get('/menus/')
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(Menu).all()
    if menus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    menu_list = [{'id': str(menu.id),
                  'title': menu.title,
                  'description': menu.description} for menu in menus]
    return menu_list


@menu_router.get("/menus/{menu_id}", response_model=CountMenuResponse, status_code=status.HTTP_200_OK)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menus = db.query(Menu).filter(Menu.id == menu_id).first()
    if menus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    submenu_count = db.query(func.count(Submenu.id)).filter(Submenu.menu_id == menus.id).scalar()
    dish_count = db.query(func.count(Dish.id)).join(Submenu).filter(Submenu.menu_id == menus.id).scalar()

    menu_data = {'id': str(menus.id),
                 'title': menus.title,
                 'description': menus.description,
                 'submenus_count': submenu_count,
                 'dishes_count': dish_count}

    return menu_data


@menu_router.post("/menus/", response_model=ResponseMenuSchema, status_code=status.HTTP_201_CREATED)
def create_menu(item: MenuSchema, db: Session = Depends(get_db)):
    menu = Menu(title=item.title, description=item.description)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    menu_data = {'id': str(menu.id),
                 'title': menu.title,
                 'description': menu.description}
    return menu_data


@menu_router.patch("/menus/{menu_id}", response_model=ResponseMenuSchema)
def update_menu(menu_id: int, item: MenuSchema, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    menu.title = item.title
    menu.description = item.description
    db.commit()
    db.refresh(menu)
    menu_data = {'id': str(menu.id),
                 'title': menu.title,
                 'description': menu.description}

    return menu_data


@menu_router.delete("/menus/{menu_id}", status_code=status.HTTP_200_OK)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    db.delete(menu)
    db.commit()
    menu_data = {'id': menu.id,
                 'title': menu.title,
                 'description': menu.description}
    return menu_data
