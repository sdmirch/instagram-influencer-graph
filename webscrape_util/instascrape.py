import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import requests
from pymongo import MongoClient

from scrape_util import setup_mongo_client, load_last_line, add_new_line

# def load_last_line(filepath):
#     """Load json in last line of given file into dictionary.
#
#     Args:
#         filepath (str): Path to file with json.
#
#     Returns:
#         last_line (dict): Last line in file loaded as a dictionary.
#
#     Usage Example:
#         user_dict = load_last_line(page_info_filepath)
#     """
#     with open(filepath, "r") as myfile:
#         last_line = json.loads(myfile.readlines()[-1])
#     return last_line
#
# def add_new_line(new_line,filepath):
#     """Add json in last line of given file as a dictionary.
#
#     Args:
#         filepath (str): Path to file with json.
#         new_line (dict): New line to be added to file.
#
#     Returns: None
#
#     Usage Example:
#         add_new_line(user_dict,page_info_filepath)
#     """
#     with open(filepath, "a") as myfile:
#         myfile.write(json.dumps(new_line) + '\n')

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

def instascrape(page_info_filepath, num_requests):
    """
    Scrape instagram hashtag search

    Args:
        page_info_filepath (str): Filepath to text file with page_info dicts
        num_requests (int): Number of pages to be scraped

    Action: saves influencer node information to pymongo database

    Output: None
    """

    client, collection = setup_mongo_client('instascrape', 'test')

    page_info = load_last_line(page_info_filepath)

    base_url_search = "https://www.instagram.com/graphql/query/?query_id=17875800862117404&variables={{%22tag_name%22:%22womenwhoclimb%22,%22first%22:{},%22after%22:%22{}%22}}"


    for i in range(num_requests):

        if page_info['has_next_page']:
            response = requests.get(base_url_search.format('12',str(page_info['end_cursor'])))

            if response.status_code == 200:
                insert_edge(response, collection)
                page_info = get_page_info(response)
                add_new_line(page_info,page_info_filepath)

            else:
                print "Status Code = " + str(response.status_code)
                return None

        time.sleep(np.random.uniform(15,45))
        print "Finished scraping {} pages of {}".format(i+1, num_requests)

    client.close()

    print "\n Finished scraping {} pages of 12 influencers each".format(num_requests)
    return None
