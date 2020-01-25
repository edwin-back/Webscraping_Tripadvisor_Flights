from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # wait until some condition is satisfied
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import csv
import time
import re

def mainscraper(dates, airports):
    # start scraping, iterating through each day as its own csv file
    # wait for flight deals to load on the page
    driver.implicitly_wait(5)

    for date in dates:
        # open a connection to a new file and write to the file
        csv_file = open('flights_{}.csv'.format(date), 'w', encoding='utf-8', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['departure_date', 'price', 'airline', 'start_airport', 'end_airport', 'start_end_time', 'duration', 'fly_score']) # input headers

        for airport in airports:
            #Iterate thru airports, non-stop flights only
            # start url
            start_url = 'https://www.tripadvisor.com/CheapFlightsSearchResults-g32655-a_airport0.NYC-a_airport1.{}-a_cos.0-a_date0.{}-a_formImp.ea52d276__2D__3c59__2D__43ff__2D__ab77__2D__96fbb1294126__2E__5810-a_nearby0.no-a_nearby1.no-a_nonstop.yes-a_pax0.a-a_travelers.1-Los_Angeles_California.html'.format(airport, date)
            driver.get(start_url)

            index = 1

            # We want to start the first couple pages.
            # while True if everything works correctly, index <= 3 otherwise for testing purposes
            while True:
                try:
                    print("Scraping Page # " + str(index) + " - NYC To {} on {}".format(airport, date))
                    print("*" * 60)
                    index += 1
                    time.sleep(1)

                    flights = driver.find_elements_by_xpath('//div[@class="flights-search-results-FlightList__listItem--3Z8uE"]')

                    for flight in flights:
                        # Initialize an empty dictionary for each flight deal
                        flight_dict = {}

                        try:
                            # requiring there to be a price b/c it will go to next flight if we can't get price
                            price = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-RightCTAColumn__price--1BJ7b"]').text
                        except:
                            continue

                        # if there is a price, then get the rest of the data for that flight deal
                        airline = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odAirline--EXFOh"]').text
                        start_airport = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odAirline--EXFOh"]/span[1]').text
                        end_airport = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odAirline--EXFOh"]/span[2]').text
                        start_end_time = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odTime--mp9Dl"]').text
                        duration = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__duration--3ITx_"]').text

                        # Some flight listings don't have a FlyScore
                        try:
                            fly_score = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-FlyScoreInfo__container--3sFJZ"]').text
                        except:
                            fly_score = 'null' # better to use np.nan for easier cleaning or manipulation later on? will it affect computation speed?
                            pass

                        # Print to console to see if features are being properly extracted
                        print('Price = {}'.format(price))
                        print('Airline = {}'.format(airline))
                        print('Start Airport = {}'.format(start_airport))
                        print('End Airport = {}'.format(end_airport))
                        print('Start and End Time = {}'.format(start_end_time))
                        print('Duration = {}'.format(duration))
                        print('Fly Score = {}'.format(fly_score))

                        # Each column of flight data to be outputted for each row as a key value pair 
                        flight_dict['departure_date'] = date
                        flight_dict['price'] = price
                        flight_dict['airline'] = airline
                        flight_dict['start_airport'] = start_airport
                        flight_dict['end_airport'] = end_airport
                        flight_dict['start_end_time'] = start_end_time
                        flight_dict['duration'] = duration
                        flight_dict['fly_score'] = fly_score

                        writer.writerow(flight_dict.values())

                    # Locate the next button element on the page and then call `button.click()` to click it.
                    # Locate the next button on the page.

                    # wait_button = WebDriverWait(driver, 10)
                    # next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="ui_button nav next primary "]')))
                    next_button = driver.find_element_by_xpath('//span[@class="ui_button nav next primary "]')
                    next_button.click()

                except Exception as e:
                    print(e)
                    break

        # close the csv file for that day
        csv_file.close()
                

# make the inital connection, open homepage
driver = webdriver.Chrome()

# NONSTOP Only, Destinations (LA (LAX), Chicago (ORD), Miami (MIA), San Juan (SJU), Montreal (YUL), London (LHR))
airports = ['LAX', 'ORD', 'MIA', 'SJU', 'YUL', 'LHR']

# jan, feb, march, april, etc.
# list(map(str,range(20200127, 20200132))) + list(map(str,range(20200201,20200230))) #
dates = list(map(str, range(20200307,20200332))) + list(map(str, range(20200401,20200431))) + list(map(str, range(20200501,20200532))) + list(map(str, range(20200601,20200631))) + list(map(str, range(20200701,20200732))) + list(map(str, range(20200801,20200832))) + list(map(str, range(20200901,20200931))) + list(map(str, range(20201001,20201032))) + list(map(str, range(20201101,20201131))) + list(map(str, range(20201201,20201232))) + list(map(str, range(20210101,20210128)))

# Execute flight scraper
start_scrape = time.time() # time started scraping
mainscraper(dates, airports) # scrape function
end_scrape = time.time() # time ended scraping
print('Total flight scrape time = {} minutes'.format((end_scrape-start_scrape)/60))  

# close the browser and end scraping
driver.close()
