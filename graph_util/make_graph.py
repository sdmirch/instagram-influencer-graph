from pymongo import MongoClient
import json
import networkx as nx

from webscrape_util.scrape_util import setup_mongo_client

def make_graph(filepath, directed=True):
    """
    Create a graph using data stored in followers collection from instacrape db.

    Args:
        filepath (str): Filepath where graph will be saved (.gml format)
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

def make_fake_graph(G, filepath, num_followers=181507):
    """
    Create a graph for testing purposes with a macro-influencer ("SelenaGomez").

    Args:
        G (nx.Graph()): Graph object, base graph of influencers and followers.
        filepath (str): Filepath where graph will be saved (.gml format)
        num_followers [Optional(int)]: Number of followers to be added from current
            follower base and to be added as fake users. Total added is 2*num_followers.

    Returns: None
    """
    G_fake = G.copy()

    G_fake.add_node("SelenaGomez")

    # Add n=181507 followers from follower base
    follower_choices = set(G.nodes()).difference(set(influencers.keys()))
    selena_followers = np.random.choice(list(follower_choices), size=181507, replace=False)

    # Add n=181507 fake followers who are not part of the follower base (not in community)
    for i in range(181507):
        random_generated_user = "Fake" + str(i)
        G_fake.add_edge(random_generated_user, "SelenaGomez")

    nx.write_gml(G_fake, filepath)
