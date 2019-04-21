from collections import defaultdict
from datetime import datetime

from flask import Flask, jsonify, Response

from bot.constants import DAYS_OF_WEEK
from bot.menu import Menus
from bot.errors import MenuError

# INIT AND CONFIG APP
APP_ADDRESS = "0.0.0.0"
APP_PORT = 8000

app = Flask(__name__)

# LOAD MENUS
menus = Menus()


@app.route(rule="/", methods=["GET", "POST"])
def welcome():
    welcome_message = "Welcome to 'What about lunch?' - a service that helps you decide where to go for lunch. "
    welcome_message += "To use the service, send a GET request to /<restaurant> or /<restaurant>/<day> endpoints."
    return jsonify(message=welcome_message)


@app.route(rule="/<string:restaurant>/<string:day>", methods=["GET"])
@app.route(rule="/<string:restaurant>", methods=["GET"])
def whats_for_lunch_today(restaurant: str, day: str = None) -> Response:
    if day is None:
        day = DAYS_OF_WEEK[datetime.today().weekday()]
    try:
        restaurant_menu = menus.menu(restaurant)
        return jsonify(lunch=restaurant_menu[day])
    except MenuError as menu_error:
        return jsonify(error=str(menu_error))
    except KeyError:
        error_msg = f"Sorry, the restaurant {restaurant} does not seem to have a menu for {day.capitalize()}."
        error_msg += " They do have a menu for: "

        for menu_day in restaurant_menu.keys():
            error_msg += menu_day.capitalize() + " "

        return jsonify(error=error_msg)


if __name__ == "__main__":

    app.run(host=APP_ADDRESS, port=APP_PORT, debug=True)
