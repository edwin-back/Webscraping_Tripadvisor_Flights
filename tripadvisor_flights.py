from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # wait until some condition is satisfied
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import csv
import time
import re

# make the inital connection, open homepage
driver = webdriver.Chrome()

# wait for flight deals to load on the page
driver.implicitly_wait(10)

# # select and click Search button
# driver.find_element_by_xpath('//button[@class="ui_button primary fullwidth"]').click()

# NONSTOP Only, Destinations (LA (LAX), Chicago (ORD), Miami (MIA), San Juan (SJU), London (LHR), Montreal (YUL))
airports = ['LAX', 'ORD', 'MIA', 'SJU', 'YUL', 'LHR']

# jan, feb, march, april, etc.
dates = list(map(str,range(20200127, 20200132))) # + list(map(str,range(20200201,20200230))) + list(map(str, range(20200301,20200332))) + list(map(str, range(20200401,20200431))) + list(map(str, range(20200501,20200532))) + list(map(str, range(20200601,20200631))) + list(map(str, range(20200701,20200732))) + list(map(str, range(20200801,20200832))) + list(map(str, range(20200901,20200931))) + list(map(str, range(20201001,20201032))) + list(map(str, range(20201101,20201131))) + list(map(str, range(20201201,20201232)))

review_urls = [] # review listings
start_scrape = time.time()

# start scraping, iterating through each day as its own csv file
for date in dates:

    # open a connection to a file and write to the file
    csv_file = open('flights_{}.csv'.format(date), 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['price', 'airline', 'start_airport', 'start_end_time', 'duration', 'stop_type', 'fly_score'])

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
                index = index + 1

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
                    stop_type = flight.find_element_by_xpath('.//div[@class="flights-search-results-itinerary-card-components-OneWayInfo__stops--1wF5n"]').text

                    # Some flight listings don't have a FlyScore

                    ############# gets huge lag time when scraper finds a flight without a fly score
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
                    print('Stop Type = {}'.format(stop_type))
                    print('Fly Score = {}'.format(fly_score))

                    # Each column of flight data to be outputted in each row as a key value pair 
                    flight_dict['price'] = price
                    flight_dict['airline'] = airline
                    flight_dict['start_airport'] = start_airport
                    flight_dict['end_airport'] = end_airport
                    flight_dict['start_end_time'] = start_end_time
                    flight_dict['duration'] = duration
                    flight_dict['stop_type'] = stop_type
                    flight_dict['fly_score'] = fly_score

                    writer.writerow(flight_dict.values())

                    # find reviews and collect ratings
                    # find and click View Deal button
                    # view_deal_button = flight.find_element_by_xpath('.//button[@class="ui_button original chevron"]')
                    # view_deal_button.click()

                # Locate the next button element on the page and then call `button.click()` to click it.
                # Locate the next button on the page.
                time.sleep(5)

                # wait_button = WebDriverWait(driver, 10)
                # next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="ui_button nav next primary "]')))
                next_button = driver.find_element_by_xpath('//span[@class="ui_button nav next primary "]')
                next_button.click()

            except Exception as e:
                print(e)
                break

    # close the csv file for that day
    csv_file.close()

end_scrape = time.time()
print('Total scrape time = {} seconds'.format(start_scrape-end_scrape))

# close the browser and end scraping
driver.close()

