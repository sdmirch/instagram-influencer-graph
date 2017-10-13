from pymongo import MongoClient
import json

from scrape_util import setup_mongo_client, write_json

def create_influencer_dict(filepath):
    """
    Create a dictionary with influencer id and posts.

    Args:
        filepath (str): Filepath where influencer dictionary will be saved

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

    write_json(influencers, filepath)
