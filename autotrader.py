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
        cars = []

        first_page_html = self.search_page_html(1)
        soup = BeautifulSoup(first_page_html, 'html.parser')

        page_counter_text = soup.find("li", {"class": "paginationMini__count"}).text
        total_pages = int(re.search(r"Page \d+ of (\d+)", page_counter_text).group(1))

        cars.extend(self.get_cars(soup))

        for i in range(total_pages - 1):
            page_number = i+2
            print "AutoTrader page " + str(page_number) + " of " + str(total_pages)
            soup = BeautifulSoup(self.search_page_html(page_number), 'html.parser')
            cars.extend(self.get_cars(soup))

        return cars


    def search_page_html(self, page_number):
        url = self.host_url + "search/used/cars/postcode/" + self.location + "/radius/" + str(self.search_radius) + "/sort/default/maximum-mileage/up_to_" + str(self.max_mileage) + "_miles/price-to/" + str(self.max_price) +"/page/" + str(page_number) + r"/onesearchad/used%2Cnearlynew%2Cnew"
        return self.get_html(url)

    def get_cars(self, soup):
        cars = []

        search_results = soup.findAll("div", {"class": "search-result__r1"})

        for search_result in search_results:
            #TODO: Also include featured ads
            if search_result.find("div", {"class": "featured-dealer__dealer-info"}):
                continue

            url = search_result.find("div", {"class": "search-results__thumbnail-col"}).find('a')['href']

            car_attributes = search_result.find("ul", {"class": "search-result__attributes"}).findAll("li")

            #I don't want to buy a car from someone who does not document its specs
            if len(car_attributes) < 6:
                continue

            #TODO: don't ignore this written-off warning!
            cat_d_warning_message = "At some point this vehicle was damaged and written off by the insurer because it was uneconomical to repair."
            if cat_d_warning_message in car_attributes[0].text:
                car_attributes.pop(0)

            year_expression = re.search(r"(\d+).+", car_attributes[0].text)
            if year_expression:
                year = int(year_expression.group(1))
            else:
                #Don't know the bleedin' year of the car? Sod off...
                continue

            car_type = car_attributes[1].text
            mileage = int(re.search(r"((?:\d+)?,?\d+)", car_attributes[2].text).group(1).replace(',',''))
            transmission = car_attributes[3].text

            engine_size = car_attributes[4].text

            #TODO: is it always electric when there < 6 attributes?
            fuel_type = car_attributes[5].text if len(car_attributes) >= 6 else "Electric??"

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
    print AutoTraderCrawler("N33JB", 1).crawl()