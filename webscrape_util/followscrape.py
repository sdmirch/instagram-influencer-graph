import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import requests
from pymongo import MongoClient

from scrape_util import (
    setup_mongo_client,
    load_json,
    load_last_line,
    add_new_line,
    load_list,
    write_text,
    selenium_instagram_login)

def find_next_influencer(filepath_influencers, filepath_scrapedinfluencers):
    """
    Finds the next influencer for followers scraping.

    Args:
        filepath_influencers (str): Filepath with ordered influencer list.
        filepath_influencers (str): Filepath with list of scraped influencers.

    Output:
        next_influencer (str): Next influencer to be scraped.
    """
    influencers_list = load_list(filepath_influencers)
    try:
        last_scraped = load_last_line(filepath_scrapedinfluencers)
        last_scraped_index = influencers_list.index(str(last_scraped))
        next_influencer = influencers_list[last_scraped_index + 1]
    except IndexError:
        next_influencer = influencers_list[0]
    return next_influencer

def load_json_from_html(driver):
    """Click on raw data and store it in json format.

    Args:
        driver (selenium webdriver): Generally initialized as Firefox.

    Returns:
        data_as_json (dict): data from raw-data tab as json.
    """
    time.sleep(np.random.uniform(1,2))
    # Clicks on raw-data tab
    driver.find_element_by_id('tab-1').click()
    data = driver.find_element_by_css_selector('pre.data')
    data_as_json = json.loads(data.text)
    return data_as_json

def insert_data(data_as_json, influencer_id, collection):
    """Insert records into Mongo database.

    Args:
        response (request response object): Response from request.get('url')
        collection (pymongo.Collection): Collection object for record insertion.
    """
    followers = data_as_json['data']['user']['edge_followed_by']['edges']
    collection.insert_one({'id':influencer_id,'follow_pack': followers})

def get_page_info(data_as_json):
    """Find and save page_info from json.

    Args:
        rdata_as_json (dict): data from raw-data tab as json.

    Returns:
        page_info (dict): Dictionary from response json.
            Keys: 'has_next_page' (bool) and 'end_cursor' (unicode)
    """
    page_info = data_as_json['data']['user']['edge_followed_by']['page_info']
    return page_info

def followscrape(num_requests):
    """
    Scrape instagram followers

    Args:
        num_requests (int): Number of influencers to be scraped

    Output: None
    """

    client, collection = setup_mongo_client('instascrape', 'followers')

    driver = webdriver.Firefox()
    selenium_instagram_login(driver, 'instagram_credentials.json')

    init_url_search = "https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables={{%22id%22:%22{}%22,%22first%22:20}}"
    base_url_search = "https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables={{%22id%22:%22{}%22,%22first%22:500,%22after%22:%22{}%22}}"

    for i in range(num_requests):
        influencer_id = find_next_influencer('data/ordered_influencers.txt', 'data/scraped_influencers.txt')

        # Initial search for followers
        driver.get(init_url_search.format(influencer_id))
        data_as_json = load_json_from_html(driver)
        insert_data(data_as_json, influencer_id, collection)
        page_info = get_page_info(data_as_json)
        page_counter = 1
        print "Finished scraping {} pages for influencer {}".format(page_counter, influencer_id)

        # Keep searching while followers still exist
        while page_info['has_next_page']:
            driver.get(base_url_search.format(influencer_id, str(page_info['end_cursor'])))
            data_as_json = load_json_from_html(driver)
            insert_data(data_as_json, influencer_id, collection)
            page_info = get_page_info(data_as_json)
            page_counter += 1
            print "Finished scraping {} pages for influencer {}".format(page_counter, influencer_id)
            time.sleep(np.random.uniform(7,10))


        write_text(influencer_id, 'data/scraped_influencers.txt')
        time.sleep(np.random.uniform(7,10))
        print "Finished scraping {} influencers of {}".format(i+1, num_requests)

    client.close()

    print "\n Finished scraping {} influencers' followers".format(num_requests)
    return None
