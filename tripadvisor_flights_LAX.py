from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # wait until some condition is satisfied
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import csv
import time
import re

# make the inital connection
driver = webdriver.Chrome()

driver.implicitly_wait(8)

# Designating NYC to LAX, 01/26/20, oneway as the first page to start scraping
# url = driver.get('https://www.tripadvisor.com/CheapFlightsSearchResults-g32655-a_airport0.NYC-a_airport1.LAX-a_cos.0-a_date0.20200126-a_formImp.ea52d276__2D__3c59__2D__43ff__2D__ab77__2D__96fbb1294126__2E__5810-a_nearby0.no-a_nearby1.no-a_nonstop.no-a_pax0.a-a_travelers.1-Los_Angeles_California.html')

## Save if needed but probably not code
# # Input destination into the 'To' search field
# destination_field = driver.find_element_by_name('To')
# destination_field.clear()
# destination_field.send_keys('MBJ')
# # select and click Search button
# driver.find_element_by_xpath('//button[@class="ui_button primary fullwidth"]').click()

# Destinations (LA, Chicago, Miami, San Juan, Ho Chi Minh City, Vancouver)
airport_codes = ['LAX', 'MDW', 'MIA', 'SJU', 'SGN', 'YVR']

# jan, feb, march, april, etc.
months = list(map(str,range(20200127, 20200132))) + list(map(str,range(20200201,20200230))) + list(map(str, range(20200301,20200332))) + list(map(str, range(20200401,20200431))) + list(map(str, range(20200501,20200532))) + list(map(str, range(20200601,20200631))) + list(map(str, range(20200701,20200732))) + list(map(str, range(20200801,20200832))) + list(map(str, range(20200901,20200931))) + list(map(str, range(20201001,20201032))) + list(map(str, range(20201101,20201131))) + list(map(str, range(20201201,20201232)))

review_urls = [] # review listings

# start scraping, iterating through each day as its own csv file
for date in months:

    # open a connection to a file and write to the file
    csv_file = open('flights_{}.csv'.format(date), 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['price', 'airline', 'start_airport', 'start_end_time', 'duration', 'stop_type', 'fly_score'])

    for airport in airport_codes:
        #Iterate thru airports
        # start url
        start_url = 'https://www.tripadvisor.com/CheapFlightsSearchResults-g32655-a_airport0.NYC-a_airport1.{}-a_cos.0-a_date0.{}-a_formImp.ea52d276__2D__3c59__2D__43ff__2D__ab77__2D__96fbb1294126__2E__5810-a_nearby0.no-a_nearby1.no-a_nonstop.no-a_pax0.a-a_travelers.1-Los_Angeles_California.html'.format(airport, date)
        driver.get(url)

        index = 1

        # We want to start the first two pages.
        # If everything works, we will change it to while True
        while index <=3:
            try:
                print("Scraping Page number " + str(index))
                print("*" * 60)
                index = index + 1
                time.sleep(3)

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
                    start_end_time = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odTime--mp9Dl"]').text
                    duration = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__duration--3ITx_"]').text
                    stop_type = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__stops--1wF5n"]').text

                    # Some flight listings don't have a FlyScore

                    ############# gets huge lag time when scraper finds a flight without a fly score
                    try:
                        fly_score = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-FlyScoreInfo__container--3sFJZ"]').text
                    except:
                        fly_score = 'NaN' # better to use np.nan for easier cleaning or manipulation later on? will it affect computation speed?
                        pass

                    # Print to console to see if features are being properly extracted
                    print('Price = {}'.format(price))
                    print('Airline = {}'.format(airline))
                    print('Start Airport = {}'.format(start_airport))
                    print('Start and End Time = {}'.format(start_end_time))
                    print('Duration = {}'.format(duration))
                    print('Stop Type = {}'.format(stop_type))
                    print('Fly Score = {}'.format(fly_score))

                    # Each column of flight data to be outputted in each row as a key value pair 
                    flight_dict['price'] = price
                    flight_dict['airline'] = airline
                    flight_dict['start_airport'] = start_airport
                    flight_dict['start_end_time'] = start_end_time
                    flight_dict['duration'] = duration
                    flight_dict['stop_type'] = stop_type
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
                csv_file.close()
                # driver.close()
                break