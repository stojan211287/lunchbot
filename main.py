import os
import requests
import PyPDF2

from bs4 import BeautifulSoup
from io import BytesIO
from datetime import date

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
            print(cycle_index)
            pdf_links[week_number] = (cycle_index, ref)
            
            week_number += 1
    
    return pdf_links


if __name__ == "__main__":
    
    FOOD_URL = "http://www.oxfordsp.com/parklife/magdalen-centre/#food"
    
    pdf_links = get_menus(food_url=FOOD_URL)

    print(pdf_links)
    
    for i, (week_number, link_data) in enumerate(pdf_links.items()):
        if i == 0:
            response = requests.get(link_data[1])
            
            pdf_file = BytesIO(response.content)
            
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            
            menu_text = pdf_reader.getPage(0).extractText().split(os.linesep)
            
            for menu_text_item in menu_text:
                print(menu_text_item.strip())

    
    
    
    
    