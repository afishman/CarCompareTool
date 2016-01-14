from gumtree import GumtreeCrawler
from autotrader import AutoTraderCrawler
import json

location = "BS28EZ"
search_radius = 50
filename = "cars.json"

crawlers = [
    AutoTraderCrawler(location, search_radius),
    GumtreeCrawler(location, search_radius)
    ]

cars=[]
for crawler in crawlers:
    cars.extend(crawler.crawl()) 

with open(filename, 'w') as outfile:
    json.dump([car.__dict__ for car in cars], outfile, indent=4)