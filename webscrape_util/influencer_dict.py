from pymongo import MongoClient
import json

from scrape_util import setup_mongo_client, write_json, write_list

def create_influencer_dict(filepath_json, return_dict=False):
    """
    Create a dictionary with influencer id and posts.

    Args:
        filepath_json (str): Filepath where influencer dictionary will be saved as json

    Action: Saves influencer dictionary to filepath.
        influencers (dict)
            Keys: id
            Values (dict):
                Keys: 'posts' (list),  'followers' (list), and 'username' (None)

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
