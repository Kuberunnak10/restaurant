from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from src.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    submenus = relationship('Submenu',
                            back_populates='menu',
                            lazy='selectin',
                            cascade='all, delete')


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    description = Column(String)

    menu = relationship('Menu',
                        back_populates='submenus',
                        lazy='selectin')

    dishes = relationship('Dish',
                          back_populates='submenu',
                          lazy='selectin',
                          cascade='all, delete')


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    submenu_id = Column(Integer, ForeignKey('submenus.id'))
    price = Column(Numeric(10, 2))

    submenu = relationship('Submenu', back_populates='dishes', lazy='selectin')
