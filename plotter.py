import json
import webbrowser
import sys

import numpy as np
import matplotlib.pyplot as plt

from car import Car


filename = "cars.json"

def onclick(event, cars):
    #Find the car closest (xdata, ydata)
    # TODO: Make this better to switch between axes
    mileage = np.array([car.year for car in cars])
    price = np.array([car.price for car in cars])


    distances = np.sqrt((mileage - event.xdata)**2 + (price - event.ydata)**2)

    closest_car = cars[distances.argmin()]

    webbrowser.open(closest_car.url)

    print "-------------------------------"
    print "Title: " + closest_car.title
    print "Url: " + closest_car.url
    print "Mileage: " + str(closest_car.mileage)
    print "Year: " + str(closest_car.year)
    print "Price: " + str(closest_car.price)

# for searching for a particular car in titles
def search(terms, string):
    if len(terms) == 0:
        return True

    lowercase = string.lower()

    for term in terms:
        if term in lowercase:
            return True

    return False

def main(search_terms):

    parsed_json = json.loads(open(filename, 'r').read())

    cars=[]
    for car in parsed_json:
        cars.append(Car(url=car['url'], 
            title=car['title'], 
            description=car['description'], 
            model=car['model'], 
            year=car['year'], 
            mileage=car['mileage'], 
            fuel_type=car['fuel_type'], 
            price=car['price']))

    filtered_cars = filter(lambda x: search(search_terms, x.title), cars)
        
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    ax.scatter([car.year for car in filtered_cars], [car.price for car in filtered_cars])
    ax.grid()
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Price')

    search_terms_message = 'Search Terms: ' + ', '.join(search_terms)
    cars_found_message = str(len(filtered_cars)) + " cars found (" + str(len(cars)) + " total)"
    ax.set_title(search_terms_message + ' | ' + cars_found_message)

    cid = fig.canvas.mpl_connect('button_release_event', lambda x: onclick(x, filtered_cars))
    
    plt.show()

if __name__ == "__main__":
    search_terms = sys.argv
    search_terms.pop(0)
    print search_terms
    main(search_terms)