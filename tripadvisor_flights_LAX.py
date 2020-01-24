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

driver.implicitly_wait(5)

# Designating NYC to LAX, 01/26/20, oneway as the first page to start scraping
driver.get('https://www.tripadvisor.com/CheapFlightsSearchResults-g32655-a_airport0.NYC-a_airport1.LAX-a_cos.0-a_date0.20200126-a_formImp.ea52d276__2D__3c59__2D__43ff__2D__ab77__2D__96fbb1294126__2E__5810-a_nearby0.no-a_nearby1.no-a_nonstop.no-a_pax0.a-a_travelers.1-Los_Angeles_California.html')

## Save if needed but probably not code
# # Input destination into the 'To' search field
# destination_field = driver.find_element_by_name('To')
# destination_field.clear()
# destination_field.send_keys('MBJ')
# # select and click Search button
# driver.find_element_by_xpath('//button[@class="ui_button primary fullwidth"]').click()

# 

# open a connection to a file and write to the file
csv_file = open('tripadvisor_flights_LAX.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['price', 'airline', 'start_airport', 'start_end_time', 'duration', 'stop_type', 'fly_score'])

index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
while index <=3:
    try:
        print("Scraping Page number " + str(index))
        print("*" * 50)
        index = index + 1

        flights = driver.find_elements_by_xpath('//div[@class="flights-search-results-FlightList__listItem--3Z8uE"]')

        for flight in flights:
            # Initialize an empty dictionary for each flight deal
            review_dict = {}

            try:
                # requiring there to be a price b/c it will go to next flight if we can't get price
                price = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-RightCTAColumn__price--1BJ7b"]').text
            except:
                continue

            # if there is a price, then get the rest of the data for that flight deal
            airline = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odAirline--EXFOh"]').text
            start_airport = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odAirline--EXFOh"]/span').text
            start_end_time = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__odTime--mp9Dl"]').text
            duration = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__duration--3ITx_"]').text
            stop_type = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__stops--1wF5n"]').text

            # Some flight listings don't have a FlyScore

            ############# gets huge lag time when scraper finds a flight without a fly score
            try:
                fly_score = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-FlyScoreInfo__container--3sFJZ"]').text
            except:
                fly_score = 'NaN' # better to use np.nan for easier cleaning or manipulation later on? will it affect computation speed?

            # Print to console to see if features are being properly extracted
            print('Price = {}'.format(price))
            print('Airline = {}'.format(airline))
            print('Start Airport = {}'.format(start_airport))
            print('Start and End Time = {}'.format(start_end_time))
            print('Duration = {}'.format(duration))
            print('Stop Type = {}'.format(stop_type))
            print('Fly Score = {}'.format(fly_score))

            # Each column of flight data to be outputted in each row as a key value pair 
            review_dict['price'] = price
            review_dict['airline'] = airline
            review_dict['start_airport'] = start_airport
            review_dict['start_end_time'] = start_end_time
            review_dict['duration'] = duration
            review_dict['stop_type'] = stop_type
            review_dict['fly_score'] = fly_score

            writer.writerow(review_dict.values())

        # Locate the next button element on the page and then call `button.click()` to click it.
        # Locate the next button on the page.
        # wait_button = WebDriverWait(driver, 10)
        # next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="ui_button nav next primary "]')))
        next_button = driver.find_element_by_xpath('//span[@class="ui_button nav next primary "]')
        next_button.click()
        time.sleep(1)

    except Exception as e:
        print(e)
        csv_file.close()
        # driver.close()
        break