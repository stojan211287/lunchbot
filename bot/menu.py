import importlib

from bot.constants import MENUS_IMPLEMENTED
from bot.errors import MenuError


class Menus:
    def __init__(self):
        self._menus = MENUS_IMPLEMENTED
        self._restaurant_modules = {}

        for menu_available in self._menus:
            self._restaurant_modules[menu_available] = importlib.import_module(
                f"bot.restaurant.{menu_available}"
            )

    def menu(self, restaurant: str) -> dict:
        if restaurant in self._menus:
            return getattr(self._restaurant_modules[restaurant], "menu")()
        else:
            raise MenuError(f"Menu for restaurant {restaurant} is not available!")
