import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import requests
from pymongo import MongoClient

from scrape_util import setup_mongo_client, load_json, load_last_line, add_new_line


def insert_edge(response, collection):
    """Insert records into Mongo database.

    Args:
        response (request response object): Response from request.get('url')
        collection (pymongo.Collection): Collection object for record insertion.
    """
    edges = response.json()['data']['hashtag']['edge_hashtag_to_media']['edges']
    for edge in edges:
        collection.insert_one(edge)

def get_page_info(response):
    """Find and save page_info from response json.

    Args:
        response (request response object): Response from request.get('url')

    Returns:
        page_info (dict): Dictionary from response json.
            Keys: 'has_next_page' (bool) and 'end_cursor' (unicode)
    """
    page_info = response.json()['data']['hashtag']['edge_hashtag_to_media']['page_info']
    return page_info

def followscrape(driver, influencer_dict_filepath):
    """
    Scrape instagram followers

    Args:
        driver (selenium webdriver): webdriver.Firefox() logged into instagram
        influencer_dict_filepath (str): Filepath to text file with influencer dicts
        num_requests (int): Number of pages to be scraped

    Action: saves influencer and follower node information to pymongo database

    Output: None
    """

    #client, collection = setup_mongo_client('instascrape', 'followers')

    influencer_dict = load_json(influencer_dict_filepath)
    influencer_ids = set(influencers.keys())

    init_url_search = "https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables={{%22id%22:%22{}%22,%22first%22:20}}"
    base_url_search = "https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables={{%22id%22:%22{}%22,%22first%22:20,%22after%22:%22{}%22}}"

    driver.get(init_url_search.format('21167060'))

    # ? How to save ids that have been checked for follower
    # ? How to check ids that have already been checked
    # ? How to modularize
    # for each id in the 1775 influencer ids:
        # check a record of all the userids already scraped to make sure this one is new
        #followers = set()
        # search followers for id, while end_cursor == True
            #driver.get(base_url_search.format(userid, end_cursor))
            #soup = BeautifulSoup(driver.page_source, 'html.parser')
            # nodes = soup.find_all('span','objectBox objectBox-string')
            # for i in range(1,len(nodes)):
            #     if (i-1)%4==0:
            #         followers.add(str(nodes[i]).split('>"')[1].split('"<')[0])
        # save the id and the followers somewhere, mongo db?, make any sets lists beforehand!


    return None




    ### Below lies unchanged instascrape stuffs
    # page_info = load_last_line(page_info_filepath)
    #
    # for i in range(num_requests):
    #
    #     if page_info['has_next_page']:
    #         response = requests.get(base_url_search.format('12',str(page_info['end_cursor'])))
    #
    #         if response.status_code == 200:
    #             insert_edge(response, collection)
    #             page_info = get_page_info(response)
    #             add_new_line(page_info,page_info_filepath)
    #
    #         else:
    #             print "Status Code = " + str(response.status_code)
    #             return None
    #
    #     time.sleep(np.random.uniform(15,45))
    #     print "Finished scraping {} pages of {}".format(i+1, num_requests)
    #
    # client.close()
    #
    # print "\n Finished scraping {} pages of 12 influencers each".format(num_requests)
    # return None
