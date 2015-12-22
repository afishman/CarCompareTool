from bs4 import BeautifulSoup
import urllib2
import ssl
import re
import json

host_url = "https://www.gumtree.com/"

def get_html(url):
    request = urllib2.urlopen(url, context=ssl._create_unverified_context())
    return request.read()

def get_links(soup):
    listing_links = soup.findAll("a", {"class": "listing-link"})
    listing_links = filter(lambda x: x['href'] != "", listing_links)

    return [link['href'] for link in listing_links]

def get_cars(soup):
    cars = []

    listing_links = soup.findAll("a", {"class": "listing-link"})
    listing_links = filter(lambda x: x['href'] != "", listing_links)

    for listing_link in listing_links:
        url = host_url + listing_link['href']
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

class Car:
    def __init__(self, url="", title="", description="", model="", year=0, mileage=0, fuel_type="", price=0):
        self.url = url
        self.title = title
        self.description = description
        self.model = model
        self.year = year
        self.mileage = mileage
        self.fuel_type = fuel_type
        self.price = price

def crawl_gumtree(location, search_radius):
    #TODO: maybe use the simpler url pattern used to get the rest of the links
    search_page_url = host_url + "search?q=&search_category=cars&search_location=" + str(location) + "&tl=&distance=" + str(search_radius)

    search_page_html = get_html(search_page_url)

    #search_page_html = open("testpage.html", 'r').read()

    soup = BeautifulSoup(search_page_html, 'html.parser')

    cars = get_cars(soup)

    #get the number of pages
    total_page_number_element = soup.find("li", {"class": "page-last hide-fully-to-l"})
    number_of_pages = int(total_page_number_element.text)

    #Get the rest of the links
    for i in range(number_of_pages - 1):
        current_page = i+2

        print "Crawling page " + str(current_page) + " of " + str(number_of_pages) 

        url = host_url + "cars/" + location + "/page" + str(current_page) + "?distance=" + str(search_radius)
        
        print url

        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        cars.extend(get_cars(soup))
        
    return cars


if __name__=="__main__":
    location = "N33JB"

    #can be 0, 1, 3, 5, 10, 15, 30, 50, 75, 100, 1000
    search_radius = 10

    cars = crawl_gumtree(location, search_radius)

    with open('GumtreeCars.json', 'w') as outfile:
        json.dump([car.__dict__ for car in cars], outfile, indent=4)