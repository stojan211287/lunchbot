import os
import requests
import PyPDF2

import typing

import logging
import daiquiri

from collections import defaultdict
from io import BytesIO
from bs4 import BeautifulSoup
from datetime import date

from bot.constants import DAYS_OF_WEEK

daiquiri.setup(level=logging.DEBUG)
logger = daiquiri.getLogger("RestaurantSadlerBrasserie")


EXCLUDED = "!"
BREAK = "__"
JOIN_NEXT_LINE = "->"
JOIN_PREVIOUS_LINE = "<-"


def get_menus(food_url):
    this_week = date.today().isocalendar()[1]

    food_site = requests.get(food_url)

    soup = BeautifulSoup(food_site.text, features="html.parser")

    menu_div = soup.findAll(
        "div", {"class": "twelve-5 nine-9 four-4 left menuDownload"}
    )[0]

    menu_links = menu_div.findChildren("ul", recursive=False)[0].findChildren(
        "li", recursive=False
    )

    pdf_links = {}
    week_number = this_week

    for link in menu_links:
        ref = link.findChildren("a", recursive=False)[0]["href"]

        if ref.split(".")[-1] == "pdf":
            cycle_index = ref.split(".")[2].split("/")[-1].split("-")[-3]
            pdf_links[week_number] = (cycle_index, ref)

            week_number += 1

    return pdf_links


def parse_dishes(food_url: str, dish_types: typing.List[str]):
    def is_line_break(line_of_menu: str, dish_types=dish_types) -> bool:
        for dish_type in dish_types:
            if line_of_menu.lower().startswith(dish_type.lower()):
                return True
        return False

    def lines_to_exclude(line_of_menu: str) -> bool:
        return (
            line_of_menu.startswith("£")
        )

    def join_next_line(line_of_menu: str) -> bool:
        return (
            line_of_menu.endswith("with")
            or line_of_menu.endswith("and")
            or line_of_menu.endswith("in")
        )

    def join_previous_line(line_of_menu: str) -> bool:
        return (
            line_of_menu.startswith("topped")
            or line_of_menu.startswith("served")
            or line_of_menu.startswith("with")
            or line_of_menu.startswith("and")
            or line_of_menu.startswith("in")
        )

    def construct_return_line(line_of_menu: str) -> str:

        return_line = line_of_menu

        if join_previous_line(return_line):
            return_line = JOIN_PREVIOUS_LINE + " " + return_line
        if join_next_line(return_line):
            return_line = return_line + " " + JOIN_NEXT_LINE

        return return_line

    def get_menu_item(line_of_menu: str) -> str:

        stripped_line = line_of_menu.strip()

        if lines_to_exclude(stripped_line):
            return EXCLUDED
        elif is_line_break(stripped_line):
            return BREAK
        else:
            return construct_return_line(stripped_line)

    def add_item_to_data_store(item: str, data_list: list) -> list:
        if not item == "":
            data_list = data_list.append(item)
        return data_list

    pdf_links = get_menus(food_url=food_url)

    dish_types = defaultdict(list)

    for i, (week_number, link_data) in enumerate(pdf_links.items()):
        # DOWNLOAD ONLY SECOND MENU - CURRENT WEEK
        if i == 1:
            # link_data IS A TUPLE - FIRST ENTRY IS INDEX OF CURRENT MENY IN AN ORDER 4 CYCLE.
            # THE SECOND IS THE LINK
            response = requests.get(link_data[1])

            pdf_file = BytesIO(response.content)

            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            menu_text = pdf_reader.getPage(0).extractText().split(os.linesep)

            # SKIP WEEK NUMBER AND WEEKDAY NAMES
            LINES_TO_SKIP = 6
            processed_items = [
                get_menu_item(menu_line) for menu_line in menu_text[LINES_TO_SKIP:]
            ]

            item_index = 0
            dish_index = 0
            parsed_menu_item = ""

            while item_index < len(processed_items):

                item = processed_items[item_index]

                if item == EXCLUDED:
                    pass
                elif item == BREAK:
                    dish_index += 1
                else:
                    parsed_menu_item = item

                    while parsed_menu_item.startswith(JOIN_PREVIOUS_LINE):
                        cut_start = len(JOIN_PREVIOUS_LINE) + 1
                        parsed_menu_item = (
                            dish_types[dish_index][-1]
                            + " "
                            + parsed_menu_item[cut_start:]
                        )
                        dish_types[dish_index].pop(-1)

                    while parsed_menu_item.endswith(JOIN_NEXT_LINE):
                        cut_end = len(JOIN_NEXT_LINE) + 1
                        parsed_menu_item = (
                            parsed_menu_item[:-cut_end]
                            + " "
                            + processed_items[item_index + 1]
                        )
                        item_index += 1

                add_item_to_data_store(parsed_menu_item, dish_types[dish_index])
                parsed_menu_item = ""

                item_index += 1

    return dish_types


def menu(food_url="https://www.oxfordsp.com/parklife/sadler-building/"):

    DISH_TYPES = [
        "Meat Main Course",
        "Vegetarian Main Course",
        "Carbohydrate",
        "Side",
    ]
    LAST_MENU_DAY_INDEX = 5

    menu = {}

    dishes = parse_dishes(food_url=food_url, dish_types=DISH_TYPES)

    logger.debug(dishes)

    restaurant_week = DAYS_OF_WEEK[:LAST_MENU_DAY_INDEX]

    incorrectly_parsed_dishes = []

    for day_index in range(len(restaurant_week)):
        day_name = restaurant_week[day_index]

        menu[day_name] = {
            f"Whole week": list(zip(dishes.values()))
        }

    return menu
