import os
import requests
import PyPDF2

from bs4 import BeautifulSoup
from io import BytesIO
from datetime import date
from collections import defaultdict


def get_menus(food_url):
    
    this_week = date.today().isocalendar()[1]
    
    food_site = requests.get(FOOD_URL)
    
    soup = BeautifulSoup(food_site.text, features="html.parser")
    
    menu_div = soup.findAll("div", {"class": "twelve-5 nine-9 four-4 left menuDownload"})[0]
    
    menu_links = menu_div.findChildren("ul" , recursive=False)[0]\
                         .findChildren("li", recursive=False)
    
    pdf_links = {}
    week_number = this_week

    for link in menu_links:
        ref = link.findChildren("a", recursive=False)[0]["href"]
        
        if ref.split(".")[-1] == "pdf":
            cycle_index = ref.split(".")[2].split("/")[-1].split("-")[-3]
            pdf_links[week_number] = (cycle_index, ref)
            
            week_number += 1
    
    return pdf_links


if __name__ == "__main__":
    
    FOOD_URL = "http://www.oxfordsp.com/parklife/magdalen-centre/#food"
    
    pdf_links = get_menus(food_url=FOOD_URL)

    EXCLUDED = "!"
    BREAK = "__"

    def lines_to_exclude(line_of_menu: str) -> bool:
        return line_of_menu.startswith("£") or \
                line_of_menu.startswith("(") or \
                line_of_menu.startswith("V") or \
                line_of_menu.startswith("GF") or \
                line_of_menu.startswith("DF") or \
                line_of_menu.startswith("H ") or \
                line_of_menu.startswith("Allergen") or \
                line_of_menu == "" or \
                line_of_menu == "H"

    def is_line_break(line_of_menu: str) -> bool:
        return line_of_menu.startswith("Meat Main Course") or \
                line_of_menu.startswith("Vegetarian Main Course") or \
                line_of_menu.startswith("Daily Snack") or \
                line_of_menu.startswith("Soup") or \
                line_of_menu.startswith("Carbohydrate") or \
                line_of_menu.startswith("Seasonal") or \
                line_of_menu.startswith("Dessert")

    def get_menu_item(line_of_menu: str) -> str:

        stripped_line = line_of_menu.strip()

        if lines_to_exclude(stripped_line):
            return EXCLUDED
        elif is_line_break(stripped_line):
            return BREAK
        else:
            return stripped_line

    data_model = defaultdict(list)
    
    for i, (week_number, link_data) in enumerate(pdf_links.items()):
        if i == 0:
            response = requests.get(link_data[1])
            
            pdf_file = BytesIO(response.content)
            
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            
            menu_text = pdf_reader.getPage(0).extractText().split(os.linesep)

            ind = 1

            for menu_text_item in menu_text[1:]:

                processed_item = get_menu_item(menu_text_item)

                if processed_item == EXCLUDED:
                    continue
                elif processed_item == BREAK:
                    ind += 1
                else:
                    data_model[ind].append(processed_item)

            for num, lst in data_model.items():
                print(num)
                print(lst)

