import os
import typing

from datetime import datetime

from fastapi import FastAPI

from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from bot.constants import DAYS_OF_WEEK
from bot.menu import Menus
from bot.errors import MenuError

# INIT AND CONFIG APP
APP_ADDRESS = "0.0.0.0"
APP_PORT = 8000

app = FastAPI()

# MOUNT STATIC FILES
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "bot", "static")), name="static")

# LOAD TEMPLATES
templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "bot", "templates"))

# LOAD MENUS
menus = Menus()


@app.get("/")
def welcome():
    welcome_message = "Welcome to 'What about lunch?' - a service that helps you decide where to go for lunch. "
    welcome_message += "To use the service, send a GET request to /<restaurant> or /<restaurant>/<day> endpoints."
    return {"message": welcome_message}


@app.get("/{restaurant}/{day}")
@app.get("/{restaurant}")
def whats_for_lunch_today(request: Request, restaurant: str, day: str = None) -> typing.Union[Response, templates.TemplateResponse]:    
    try:
        restaurant_menu = menus.menu(restaurant)
        pretty_restaurant_name = " ".join(
            [word.capitalize() for word in restaurant.split("_")]
        )

        import os
        print(f"Dir is {os.getcwd()}")

        if day is None:
            return templates.TemplateResponse("table.html", {"request": request, "menu": restaurant_menu})
        else:
            response_dict = {
                f"Lunch at {pretty_restaurant_name} on {day.capitalize()}": restaurant_menu[
                    day
                ]
            }
        return response_dict

    except MenuError as menu_error:
        return {"error": str(menu_error)}

    except KeyError:
        error_msg = f"Sorry, the restaurant {restaurant} does not seem to have a menu for {day.capitalize()}."
        error_msg += " They do have a menu for: "

        for menu_day in restaurant_menu.keys():
            error_msg += menu_day.capitalize() + " "

        return {"error": error_msg}


