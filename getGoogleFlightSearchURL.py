#! /usr/bin/env python

import datetime
import sys

from playwright.sync_api import sync_playwright, TimeoutError
from tripTypes import TripTypes

def fillin_search_flights_info(page, from_to_airports: tuple[str, str], date_start_str, date_return_str) -> (bool, str):
    try:
        airport_from, airport_to = from_to_airports
        date_start = datetime.datetime.strptime(date_start_str.strip(), "%Y/%m/%d")
        print('date_start=', date_start, date_start.strftime('%b %d, %Y'))
        if date_return_str and date_return_str.strip() != '':
            trip_type = TripTypes.ROUND_TRIP
            date_return = datetime.datetime.strptime(date_return_str.strip(), "%Y/%m/%d")
            print('date_return=', date_return, date_return.strftime('%b %d, %Y'))
        else:
            trip_type = TripTypes.ONE_WAY

        page.goto('https://www.google.com/travel/flights')
    
        # select trip type
        page.click('//span[text()="Round trip"]')
        page.click('//li[@role="option" and text()="{}"]'.format(trip_type.value))

        # enter departure airport in search
        page.click('//div[@aria-placeholder="Where from?"]')
        ###page.wait_for_timeout(500)
        page.keyboard.type(airport_from)
        page.press('//div[@aria-placeholder="Where from?"]', 'Enter')
        ###page.wait_for_timeout(1000)

        # enter destination airport in search
        page.click('//div[@aria-placeholder="Where to?"]')
        ###page.wait_for_timeout(500)
        page.keyboard.type(airport_to)
        page.press('//div[@aria-placeholder="Where to?"]', 'Enter', delay=100)
        ###page.wait_for_timeout(1000)

        # enter departure date
        page.click('//input[@placeholder="Departure"]')
        ###page.wait_for_timeout(2000)
        page.keyboard.press('Control+A')
        page.keyboard.type(date_start.strftime('%b %d, %Y'))

        # set return date if round trip
        if trip_type == TripTypes.ROUND_TRIP:
            page.keyboard.press('Tab')
            page.click('(//input[@placeholder="Return"])[2]')
            page.keyboard.press('Control+A')
            ###page.wait_for_timeout(2000)
            page.keyboard.type(date_return.strftime('%b %d, %Y'))
        
        # click search button
        for _ in range(5):
            ###page.wait_for_timeout(300)
            page.keyboard.press('Enter')

        success, msg = True, page.url
    except:
        error_msg = sys.exc_info()[1]
        success, msg = False, error_msg
        pass # sys.exc_clear()

    return success, msg

# TODO - get the field values from the page and compare to intended ones
def verify_search_url():
    print('TODO verify_search_url()')

def create_browser_page() -> str:
    # To launch an invisible browser, use headless=True
    browser = p.firefox.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    return page

def main(page, from_to_airports_combination, date_start_str, date_return_str):
    success, url = fillin_search_flights_info(page, from_to_airports_combination, date_start_str, date_return_str)
    ###page.wait_for_timeout(5000)
    if (success):
        print('url = ', url)
        print('pageurl = ', page.url)
    else:
        print('Error: ', url)
    verify_search_url()

if __name__ == '__main__':
    with sync_playwright() as p:
        page = create_browser_page()
        # Currently only one airport code is supported for departure and destination (like "NYC" but not "JFK,LGA").
        # TODO: Support multiple airport codes for departure and destination.
        from_to_airports_combination=("DEN", "NYC")
        print('from_to_airports_combination=', from_to_airports_combination)
        main(page, from_to_airports_combination, '  2023/7/4        ', ' 2023/8/24     ')
    print('Job done')
