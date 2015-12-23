from bs4 import BeautifulSoup
import urllib2
import ssl
import re
import json

from crawler import Crawler
from car import Car

class GumtreeCrawler(Crawler):
    host_url = "https://www.gumtree.com/"

    def __init__(self, location, search_radius):
        self.location = location
        self.search_radius = search_radius

    def crawl(self):
        #TODO: maybe use the simpler url pattern used to get the rest of the links
        search_page_url = self.host_url + "search?q=&search_category=cars&search_location=" + str(self.location) + "&tl=&distance=" + str(self.search_radius)

        search_page_html = self.get_html(search_page_url)

        #search_page_html = open("testpage.html", 'r').read()

        soup = BeautifulSoup(search_page_html, 'html.parser')

        cars = self.get_cars(soup)

        #get the number of pages
        total_page_number_element = soup.find("li", {"class": "page-last hide-fully-to-l"})
        number_of_pages = int(re.search(r"((?:\d+)?,?\d+)", total_page_number_element.text).group(1).replace(',',''))

        #Get the rest of the links
        for i in range(number_of_pages - 1):
            current_page = i+2

            print "Gumtree page " + str(current_page) + " of " + str(number_of_pages) 

            url = self.host_url + "cars/" + self.location + "/page" + str(current_page) + "?distance=" + str(self.search_radius)

            html = self.get_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            cars.extend(self.get_cars(soup))
            
        return cars


    def get_links(self, soup):
        listing_links = soup.findAll("a", {"class": "listing-link"})
        listing_links = filter(lambda x: x['href'] != "", listing_links)

        return [link['href'] for link in listing_links]

    def get_cars(self, soup):
        cars = []

        listing_links = soup.findAll("a", {"class": "listing-link"})
        listing_links = filter(lambda x: x['href'] != "", listing_links)

        for listing_link in listing_links:
            url = self.host_url + listing_link['href']
            title = listing_link.find("h2", {"class":"listing-title", "itemprop":"name"}).text
            description = listing_link.find("p", {"itemprop": "description"}).text
            year = int(listing_link.find("span", {"itemprop": "releaseDate"}).text)
            
            mileage_text = listing_link.find("span", {"itemprop":"vehicleMileage"}).text
            mileage = int(re.search(r"((?:\d+)?,?\d+)", mileage_text).group(1).replace(',',''))

            fuel_type_element = listing_link.find("span", {"itemprop":"vehicleFuelType"})
            fuel_type = fuel_type_element.text if fuel_type_element else ""

            price_text = listing_link.find("strong", {"itemprop":"price"}).text
            price = int(re.search(r"((?:\d+)?,?\d+)", price_text).group(1).replace(',',''))

            cars.append(Car(url=url, 
                title=title, 
                description=description, 
                year=year, 
                mileage=mileage, 
                fuel_type=fuel_type, 
                price=price))

        return cars


if __name__ == "__main__":
    location = "N33JB"

    #can be 0, 1, 3, 5, 10, 15, 30, 50, 75, 100, 1000
    search_radius = 10

    cars = GumtreeCrawler().crawl(location, search_radius)

    print cars