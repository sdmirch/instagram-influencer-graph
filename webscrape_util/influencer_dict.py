from pymongo import MongoClient
import json
import networkx as nx
from collections import Counter

from scrape_util import setup_mongo_client, write_json, write_list

def create_influencer_dict(filepath_json, return_dict=False):
    """
    Create a dictionary with influencer id and posts.

    Args:
        filepath_json (str): Filepath where influencer dictionary will be saved as json.

    Action: Saves influencer dictionary to filepath.
        influencers (dict)
            Keys: id
            Values (dict):
                Keys: 'posts' (list),  'followers' (list)

    Output: None
    """

    client, collection = setup_mongo_client('instascrape', 'test')

    # Retrieve shortcodes and ids from influencers in MongoDB
    shortcodes_ids = []
    cursor = collection.find({})
    for x in cursor:
        shortcodes_ids.append((str(x['node']['shortcode']), str(x['node']['owner']['id'])))

    # Create influencers dictionary
    influencers = {}
    for sc_id_tuple in shortcodes_ids:
        if sc_id_tuple[1] in influencers:
            influencers[sc_id_tuple[1]]['posts'].append(sc_id_tuple[0])
        else:
            influencers[sc_id_tuple[1]] = {'posts':[sc_id_tuple[0]]}

    # Remove profiles that have been deleted since initial scraping
    del influencers['4018066784']

    write_json(influencers, filepath_json)

    client.close()

    if return_dict:
        return influencers


def order_influencers(filepath_json, filepath_txt):
    """
    Write influencer ids, sorted by number of posts, to a text file.

    Args:
        filepath_json (str): Filepath where influencer dictionary will be saved as json
        filepath (str): Filepath where sorted influencer ids will be saved.

    Output: None
    """

    influencers = create_influencer_dict(filepath_json, return_dict=True)

    #Sort influencers by number of posts
    inf_sort = sorted(influencers, key=lambda x: len(influencers[x]['posts']), reverse=True)

    write_list(inf_sort, filepath_txt)

def add_hashtag_posts_likes(d, user_id, x):
    """
    Utility function for create_hashtag_likes_dict.py, adds data to dictionary.

    Args:
        d (dict): Influencer dictionary.
        user_id (str): user_id for key.
        x (dict): MongoDB json record.
    """
    if len(x['node']['edge_media_to_caption']['edges']) != 0:
        text = x['node']['edge_media_to_caption']['edges'][0]['node']['text'].split("#")
        for item in text:
            if len(item.split()) == 1:
                d[user_id]['hashtags'].append(item)
    d[user_id]['posts'].append(x['node']['shortcode'])
    d[user_id]['likes'].append(x['node']['edge_liked_by']['count'])

def create_hashtag_likes_dict(filepath_json, return_dict=False):
    """
    Create a dictionary with influencer id, hashtags, posts, and
    number of likes for each post.

    Args:
        filepath_json (str): Filepath where dictionary will be saved as json.

    Action: Saves influencer dictionary to filepath.
        influencers (dict)
            Keys: id
            Values (dict):
                Keys: 'hashtags' (list), posts (list),  'likes' (list)

    Output: None
    """

    client, collection = setup_mongo_client('instascrape', 'test')

    influencers = {}
    cursor = collection.find({})
    for x in cursor:
        user_id = x['node']['owner']['id']
        if user_id in influencers:
            add_hashtag_posts_likes(influencers, user_id, x)
        else:
            influencers[user_id] = {'hashtags':[],'posts':[], 'likes':[]}
            add_hashtag_posts_likes(influencers, user_id, x)

    # Remove profiles that have been deleted since initial scraping
    del influencers['4018066784']

    client.close()

    write_json(influencers, filepath_json)

    if return_dict:
        return influencers

def list_of_hashtags(d):
    """
    Create a list of all the hashtags.

    Args:
        d (dict): Dictionary in format of returned object from
        create_hashtag_likes_dict.

    Output:
        total_hashtags (list): List of all hashtags used.
    """
    total_hashtags = []
    for value_dict in d.values():
        for hashtag in value_dict['hashtags']:
            total_hashtags.append(hashtag)
    return total_hashtags

def count_hashtags(total_hashtags):
    """
    Create Counter dictionary for hashtags.

    Args:
        total_hashtags (list): List of all hashtags used.

    Output:
        c (Counter): Counter dictionary with hashtags and frequency.
    """
    words_to_count = (word.lower() for word in total_hashtags)
    c = Counter(words_to_count)
    return c

def add_total_followers(G, d):
    """
    Add total number of followers to a dictionary.

    Args:
        G (nx.Graph()): Graph object.
        d (dict): Dictionary, generally with hastags, likes, and posts.

    Output: None
    """
    for influencer in d:
        d[influencer]['num_follow'] = len(G.in_edges(influencer))
    return d
