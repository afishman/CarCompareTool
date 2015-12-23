import json
import webbrowser

import numpy as np
import matplotlib.pyplot as plt

from car import Car

search_terms = ["accord"]
filename = "cars.json"

def onclick(event, cars):
    #Find the car closest (xdata, ydata)
    mileage = np.array([car.mileage for car in cars])
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

def search(terms, string):
    if len(terms) == 0:
        return True

    lowercase = string.lower()

    for term in terms:
        if term in lowercase:
            return True

    return False

if __name__ == "__main__":
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
    
    cars_found_message = str(len(filtered_cars)) + " cars found (" + str(len(cars)) + " total)"
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111)
    ax.scatter([car.mileage for car in filtered_cars], [car.price for car in filtered_cars])
    ax.grid()
    
    ax.set_xlabel('Mileage')
    ax.set_ylabel('Price')
    search_terms_message = 'Search Terms: ' + ', '.join(search_terms)
    ax.set_title(search_terms_message + ' | ' + cars_found_message)

    cid = fig.canvas.mpl_connect('button_release_event', lambda x: onclick(x, filtered_cars))
    
    plt.show()