from time import sleep 
from selenium import webdriver
import random
from bs4 import BeautifulSoup
import pandas as pd

class RealEstate:

    def __init__(self,district,max_pages):
        self.district = district
        self.page_number = 1  # Start from the first page
        self.max_pages = max_pages-1  # Set the maximum number of pages
        self.font_base = f'https://www.immobiliare.it/en/vendita-case/{district}/?pag='
        self.driver = self.settings()

        self.description_ls = []
        self.rooms_ls = []
        self.m2_ls = []
        self.bathroom_ls = []
        self.price_ls = []
        self.link_ls = []

    def settings(self):
        chrome_driver_path = "/usr/bin/chromedriver"
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            # Adicione mais user-agents se necessário
        ]

        random_user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"user-agent={random_user_agent}")

        sleep(random.uniform(2,5))

        return webdriver.Chrome(options=chrome_options)

    def collect_data(self):
        while True:
            font = f'{self.font_base}{self.page_number}'
            self.driver.get(font)
            sleep(10)
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            block = soup.find("main",attrs={"class":"in-listAndMapMain"}) # Mainly block to colect the data
            informations = block.find_all("div",attrs={"class":"nd-mediaObject__content in-reListCard__content is-spaced"}) # Block that contain informations
            if not informations or self.page_number > self.max_pages:
                # Break the loop if there's no more data or reached the maximum pages
                break
            for data in informations:
                description = data.find("a",attrs={"class":"in-reListCard__title"})
                features = data.find_all("li", attrs={"class": "nd-list__item in-feat__item"})
                if len(features) >= 3:
                    rooms, m2, bathrooms = features[:3]
                else:
                    # Handle the case where there are not enough elements
                    rooms = m2 = bathrooms = None  # You can use a default value or None

                price = data.find("div",attrs={"class":"in-reListCardPrice"})
                link = data.find('a', attrs={'href': True})

                self.description_ls.append(description.text)
                if rooms:
                    for room in rooms:
                        self.rooms_ls.append(room.text)
                else:
                    self.rooms_ls.append(None)
                
                if m2:
                    for m in m2:
                        self.m2_ls.append(m.text)
                        # Extract bathrooms information or append a placeholder if not found
                else:
                    self.m2_ls.append(None)
                if bathrooms:
                    for bathroom in bathrooms:
                        self.bathroom_ls.append(bathroom.text)
                else:
                    self.bathroom_ls.append(None)  # Placeholder for null value

                self.price_ls.append(price.text)
                self.link_ls.append(link['href'])

            self.page_number += 1

    def DataFrame(self):
        
        dic = {"description":self.description_ls,
               "rooms":self.rooms_ls,
               "m2":self.m2_ls,
               "bathrooms":self.bathroom_ls,
               "price":self.price_ls,
               "links":self.link_ls}

        df = pd.DataFrame(dic)
        df.to_csv(f"{self.district}.csv")


if __name__=='__main__':
    real_state = RealEstate('milano',80)
    real_state.collect_data()
    real_state.DataFrame()
