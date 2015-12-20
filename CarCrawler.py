from bs4 import BeautifulSoup
import urllib2
import ssl
import re

def get_html(url):
    request = urllib2.urlopen(url, context=ssl._create_unverified_context())
    return request.read()

def get_links(soup):
    listing_links = soup.findAll("a", {"class": "listing-link"})
    listing_links = filter(lambda x: x['href'] != "", listing_links)

    links = [link['href'] for link in listing_links]

    return links

def get_cars(soup):
    cars = []

    listing_links = soup.findAll("a", {"class": "listing-link"})
    listing_links = filter(lambda x: x['href'] != "", listing_links)

    for listing_link in listing_links:
        url = listing_link['href']
        title = listing_link.find("h2", {"class":"listing-title", "itemprop":"name"}).text
        description = listing_link.find("p", {"itemprop":"description"}).text
        year = int(listing_link.find("span", {"itemprop":"releaseDate"}).text)
        
        mileage_text = listing_link.find("span", {"itemprop":"vehicleMileage"}).text
        mileage = int(re.search(r"(\d+,\d+)", mileage_text).group(1).replace(',',''))

        fuel_type = listing_link.find("span", {"itemprop":"vehicleFuelType"}).text

        price_text = listing_link.find("strong", {"itemprop":"price"}).text
        price = int(re.search(r"(\d+,\d+)", price_text).group(1).replace(',',''))

        print price
        break

    return cars

class Car:
    def __init__(self, description="", url="", title="", model="", year=0, mileage=0, price=0):
        self.description = description
        self.url = url
        self.title = title
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price


host_url = "https://www.gumtree.com/"
location = "BS28EZ"

#can be 0, 1, 3, 5, 10, 15, 30, 50, 75, 100, 1000
search_radius = 1

#TODO: maybe use the simpler url pattern used to get the rest of the links
search_page_url = host_url + "search?q=&search_category=cars&search_location=" + str(location) + "&tl=&distance=" + str(search_radius)

print search_page_url

#search_page_html = get_html(search_page_url)
search_page_html = open("testpage.html", 'r').read()

soup = BeautifulSoup(search_page_html, 'html.parser')

cars = get_cars(soup)
print 1/0

#Get the links on that page
links=[]
links.append(get_links(soup))

#Get the number of pages
#total_page_number_element = soup.find("form", {"class": "to-select-wrapper"})
#m = re.search(r"of (\d+)", total_page_number_element.text)
#number_of_pages = int(m.group(1))

total_page_number_element = soup.find("li", {"class": "page-last hide-fully-to-l"})
number_of_pages = int(total_page_number_element.text)

print "Number of pages: " + str(number_of_pages)

#Get the rest of the links
for i in range(number_of_pages - 1):
    url = host_url + "cars/" + location + "/page" + str(i) + "?distance=" + str(search_radius)
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    link = get_links(soup)
    links.append(link)

print links
#listings = soup.findAll("h2", {"class": "listing-title"})
#listings = filter(lambda x: not any(x.findAll('span')), listings)

#
#for listing in listings:
#    print listing.text

