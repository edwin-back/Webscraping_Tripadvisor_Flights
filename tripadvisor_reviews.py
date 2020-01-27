from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # wait until some condition is satisfied

import csv
import time
import re

# make the inital connection, open homepage
driver = webdriver.Chrome()

# manually had to get urls b/c there is a proprietary code built into the url that starts with a 'd' followed by an ambiguous combo of integers
review_urls = ['https://www.tripadvisor.com/Airline_Review-d8729177-Reviews-United-Airlines#REVIEWS','https://www.tripadvisor.com/Airline_Review-d8729017-Reviews-Alaska-Airlines#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729020-Reviews-American-Airlines#REVIEWS','https://www.tripadvisor.com/Airline_Review-d8729099-Reviews-JetBlue#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729157-Reviews-Spirit-Airlines#REVIEWS', 'https://www.tripadvisor.com/Airline_Review-d8729213-Reviews-Frontier-Airlines#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729060-Reviews-Delta-Air-Lines#REVIEWS', 'https://www.tripadvisor.com/Airline_Review-d8729186-Reviews-WestJet#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8728998-Reviews-Air-Canada#REVIEWS', 'https://www.tripadvisor.com/Airline_Review-d8729182-Reviews-Virgin-Atlantic-Airways#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729039-Reviews-British-Airways#REVIEWS', 'https://www.tripadvisor.com/Airline_Review-d8729113-Reviews-Lufthansa#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729027-Reviews-Austrian-Airlines#REVIEWS', 'https://www.tripadvisor.com/Airline_Review-d8729089-Reviews-Iberia#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729078-Reviews-Finnair#REVIEWS', 'https://www.tripadvisor.com/Airline_Review-d8729003-Reviews-Air-France#REVIEWS',\
'https://www.tripadvisor.com/Airline_Review-d8729104-Reviews-KLM-Royal-Dutch-Airlines#REVIEWS']

csv_file = open('airline_reviews.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['airline_name', 'num_reviews', 'overall_rating', 'legroom', 'seat_comfort', 'entertainment', 'onboard_experience', 'customer_service', 'value_for_money', 'cleanliness', 'checkin_and_boarding', 'food_and_bev']) # input headers

# Execute review scraper
try:
    for url in review_urls:
        driver.get(url)
        review_dict = {}

        airline_name = driver.find_element_by_xpath('//h1[@class="flights-airline-review-page-airline-review-header-AirlineDetailHeader__airlineName--2JeT1"]').text
        num_reviews = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__num_reviews--3Tj5J"]').text
        overall_rating = driver.find_element_by_xpath('//div[@class="flights-airline-review-page-overview-module-OverviewModule__overall_rating--30Bld"]/span[1]').text
        legroom = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][1]/span').get_attribute('class')
        seat_comfort = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][2]/span').get_attribute('class')
        entertainment = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][3]/span').get_attribute('class')
        onboard_exp = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][4]/span').get_attribute('class')
        customer_service = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][5]/span').get_attribute('class')
        value_for_money = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][6]/span').get_attribute('class')
        cleanliness = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][7]/span').get_attribute('class')
        checkin_and_boarding = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][8]/span').get_attribute('class')
        food_and_bev = driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__rating--2tfWJ"][9]/span').get_attribute('class')
        
        review_dict['airline_name'] = airline_name
        review_dict['num_reviews'] = num_reviews
        review_dict['overall_rating'] = overall_rating
        review_dict['legroom'] = legroom
        review_dict['seat_comfort'] = seat_comfort
        review_dict['entertainment'] = entertainment
        review_dict['onboard_experience']
        review_dict['customer_service'] = customer_service
        review_dict['value_for_money'] = value_for_money
        review_dict['cleanliness'] = cleanliness
        review_dict['checkin_and_boarding'] = checkin_and_boarding
        review_dict['food_and_bev'] = food_and_bev

        writer.writerow(review_dict.values())

except Exception as e:
    print(e)
    pass

csv_file.close()

