from time import sleep 
from selenium import webdriver
import random
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from urllib.parse import urlparse

class RealEstate:

    def __init__(self,district):
        self.district = district
        self.page_number = 1  # Start from the first page
        #self.max_pages = max_pages-1  # Set the maximum number of pages
        self.font_base = f'https://www.immobiliare.it/en/vendita-case/milano/{self.district}/?pag='
        self.driver = self.settings()

        self.day = []
        self.district_ls = []
        self.description_ls = []
        self.rooms_ls = []
        self.m2_ls = []
        self.bathroom_ls = []
        self.price_ls = []
        self.link_ls = []

        self.today = date.today()

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
            n_pages = soup.find('div',attrs={"class":"in-pagination in-searchListMainContent__pagination"})
            #print(n_pages)
            n_page = list(n_pages.find('div',attrs={"class":"in-pagination__list"}))
            page = n_page[-1].text
            if not informations or self.page_number > (int(page)-1):
                # Break the loop if there's no more data or reached the maximum pages
                break
            for data in informations:

                self.day.append(self.today)
                self.district_ls.append(self.district)
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
        self.driver.close()

    def DataFrame(self):
        
        dic = {"day":self.day,
               "district":self.district_ls,
               "description":self.description_ls,
               "rooms":self.rooms_ls,
               "m2":self.m2_ls,
               "bathrooms":self.bathroom_ls,
               "price":self.price_ls,
               "links":self.link_ls}

        df = pd.DataFrame(dic)

        # Função para extrair o último número da URL
        def extract_house_id(url):
            parsed_url = urlparse(url)
            path_segments = parsed_url.path.split('/')
            for segment in reversed(path_segments):
                if segment.isdigit():
                    return int(segment)
            return None

        # Aplicar a função à coluna 'links' para criar a coluna 'house_id'
        df['house_id'] = df['links'].apply(extract_house_id)
        df.to_csv("/home/the-lord/Documents/Europe-Real-Estate/data_treatment/{}_{}.csv".format(self.district, self.today), index=False)


if __name__=='__main__':

    medaglie_d_oro = RealEstate('porta-romana-medaglie-d-oro')
    medaglie_d_oro.collect_data()
    medaglie_d_oro.DataFrame()

    cadore_montenero = RealEstate('porta-romana-cadore-montenero')
    cadore_montenero.collect_data()
    cadore_montenero.DataFrame()