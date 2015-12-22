from crawler import Crawler
from bs4 import BeautifulSoup
import re

from car import Car

class AutoTraderCrawler(Crawler):
    host_url = "http://www.autotrader.co.uk/"

    max_mileage = 100000
    max_price = 8000

    def __init__(self, location, search_radius):
        self.location = location
        self.search_radius = search_radius

    def crawl(self):
        first_page_html = self.search_page_html(1)

        soup = BeautifulSoup(first_page_html, 'html.parser')

        page_counter_text = soup.find("li", {"class": "paginationMini__count"}).text
        total_pages = int(re.search(r"Page \d+ of (\d+)", page_counter_text).group(1))

        #for i in range(total_pages - 1)

        print self.get_cars(soup)

        return "carrrrs"


    def search_page_html(self, page_number):
        url = "search/used/cars/postcode/" + self.location + "/radius/" + str(self.search_radius) + "/sort/default/maximum-mileage/up_to_" + str(self.max_mileage) + "_miles/price-to/" + str(self.max_price) +"/page/" + str(page_number) + r"/onesearchad/used%2Cnearlynew%2Cnew"
        return self.get_html(self.host_url + url)

    def get_cars(self, soup):
        cars = []

        search_results = soup.findAll("div", {"class": "search-result__r1"})

        for search_result in search_results:
            url = search_result.find("div", {"class": "search-results__thumbnail-col"}).find('a')['href']

            car_attributes = search_result.find("ul", {"class": "search-result__attributes"}).findAll("li")

            year = int(re.search(r"(\d+) \(\d+", car_attributes[0].text).group(1))
            car_type = car_attributes[1].text
            mileage = int(re.search(r"((?:\d+)?,?\d+)", car_attributes[2].text).group(1).replace(',',''))
            transmission = car_attributes[3].text
            engine_size = car_attributes[4].text
            fuel_type = car_attributes[5].text

            description = search_result.find("p", {"class": "search-result__description"}).text

            title = search_result.find("h1", {"class": "search-result__title"}).text

            price_text = search_result.find("div", {"class": "search-result__price"}).text
            price = int(re.search(r"((?:\d+)?,?\d+)", price_text).group(1).replace(',',''))

            cars.append(Car(url=url, 
                title=title, 
                description=description, 
                year=year, 
                mileage=mileage, 
                fuel_type=fuel_type, 
                price=price))

        return cars

if __name__=="__main__":
    AutoTraderCrawler("N33JB", 1).crawl()