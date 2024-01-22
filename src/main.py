from fastapi import FastAPI

from src.restaurant_api.routers.dish import dish_router
from src.restaurant_api.routers.submenu import submenu_router
from src.restaurant_api.routers.menu import menu_router

app = FastAPI()

app.include_router(menu_router, prefix='/api/v1')
app.include_router(submenu_router, prefix='/api/v1/menus')
app.include_router(dish_router, prefix='/api/v1/menus')
