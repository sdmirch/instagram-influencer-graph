from pymongo import MongoClient
import json
import networkx as nx

from webscrape_util.scrape_util import setup_mongo_client

def make_graph(filepath, directed=True):
    """
    Create a graph using data stored in followers collection from instacrape db.

    Args:
        filepath (str): Filepath where graph will be save (.gml format)
        directed (Optional[bool]): Creates directed graph by default.

    Returns: None
    """
    client, collection = setup_mongo_client('instascrape', 'followers')

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    cursor = collection.find({})
    for record in cursor:
        influencer = record['id']
        for follower in (record['follow_pack']):
            G.add_edge(follower['node']['id'], influencer)

    nx.write_gml(G, filepath)
