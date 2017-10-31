import networkx as nx
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from webscrape_util.scrape_util import load_json

def reduce_by_critical_mass(G, crit_mass=5000):
    """
    Reduces graph by removing nodes that have less than a specific number of
        followers (critical mass, default=5000).

    Args:
        G (nx.Graph()): Graph object, with all influencers and followers.
        crit_mass (Optional[int]): Critical mass following, default 5000.

    Returns:
        G_reduced (nx.Graph()): Graph object, containing only nodes with more
            than critical mass of followers.
    """
    G_reduced = G.copy()

    G_nodes = set(G.nodes())
    for node in G_nodes:
        if len(G.in_edges(node)) < crit_mass:
            G_reduced.remove_node(node)
    return G_reduced

def calc_community_influence_score(G,returned='list'):
    """
    Calculate and sort by community influence scores, which is eigenvector centrality
        for a graph (higher scores for higher eigenvector centralities).

    Args:
        G (nx.Graph()): Graph object.
        returned [Optional(list)]: 'list' or 'dict' will change data structure returned.

    Returns:
        sorted_influence_score (list of tuples): List of nodes sorted by eigenvector
            centrality.
    """

    c = nx.eigenvector_centrality(G)
    if returned == 'list':
        sorted_influence_score = (sorted(c.iteritems(), key=lambda x: x[1], reverse=True))
        return sorted_influence_score
    else:
        return c

def calc_interaction_score(G, d, returned='list'):
    """
    Calculate and sort by interaction scores for reduced graph based
        on likes and followers (higher scores for larger likes to followers ratios).

    Args:
        G (nx.Graph()): Graph object.
        d (dict): Dictionary with user ids, number of likes, and number of followers.
        returned [Optional(list)]: 'list' or 'dict' will change data structure returned.

    Returns:
        sorted_interaction_score
    """
    interaction_score = {}

    for user_id in G.nodes():
        if user_id == 'SelenaGomez':
            # Add Selena Gomez for test
            interaction_score['SelenaGomez'] = 0.05
        else:
            interaction_score[user_id] = (1.0*d[user_id]['max_likes']/d[user_id]['num_follow'])

    if returned == 'list':
        sorted_interaction_score = (sorted(interaction_score.iteritems(), key=lambda x: x[1], reverse=True))
        return sorted_interaction_score
    else:
        return interaction_score

def calc_authenticity_score(G, captions, returned='list'):
    """
    Calculate and sort by authenticity scores for reduced graph based
        on compound sentiment analysis score (higher scores for more negative posts).

    Args:
        G (nx.Graph()): Graph object.
        captions (dict): Dictionary with user ids and captions.
        returned [Optional(list)]: 'list' or 'dict' will change data structure returned.

    Returns:
        sorted_authenticity_score
    """
    analyzer = SentimentIntensityAnalyzer()
    top_influencers = G.nodes()
    top_influencers.remove("SelenaGomez")

    caption_sentiment = {}
    for user_id in top_influencers:
        for caption in captions[user_id]['caption']:
            vs = analyzer.polarity_scores(caption)
            if user_id in caption_sentiment:
                caption_sentiment[user_id].append(vs)
            else:
                caption_sentiment[user_id] = [vs]

    caption_sentiment_means = {}
    for user_id in caption_sentiment:
        df = pd.DataFrame(caption_sentiment[user_id])
        # Subtract compound score from 1 to penalize more positive captions
        caption_sentiment_means[user_id] = 1 - dict(df.mean())['compound']
    # Add Selena Gomez for test
    caption_sentiment_means["SelenaGomez"] = 0.5

    if returned == 'list':
        sorted_authenticity_score = (sorted(caption_sentiment_means.iteritems(), key=lambda x: x[1], reverse=True))
        return sorted_authenticity_score
    else:
        return caption_sentiment_means

def normalize_values(d):
    """
    Return dictionary with normalized values (0 to 1).

    Args:
        d (dict): Dictionary with user ids and raw scores.

    Returns:
        d_norm (dict): Dictionary with user ids and normalized scores.
    """
    minimum = min(d.iteritems(), key= lambda x: x[1])[1]
    maximum = max(d.iteritems(), key= lambda x: x[1])[1]

    d_norm = {}
    for user_id in d:
        d_norm[user_id] = (d[user_id] - minimum) / (maximum - minimum)

    return d_norm

def calc_overall_score(influence_score, interaction_score, authenticity_score):
    """
    Calculate overall scores and save all types of scores to one dictionary.

    Args:
        influence_score (dict): Dictionary with user ids and influence scores.
        interaction_score (dict): Dictionary with user ids and interaction scores.
        authenticity_score (dict): Dictionary with user ids and authenticity scores.

    Returns:
        scores (dict): Dictionary with all score types, and final scores.
    """
    scores = {}
    users = influence_score.keys()

    # Normalize scores dictionaries
    influence_normed = normalize_values(influence_score)
    interaction_normed = normalize_values(interaction_score)
    authenticity_normed = normalize_values(authenticity_score)

    # Add normalized scores types to scores
    for user_id in users:
        scores[user_id] = {'influence':None, 'interaction':None,
                            'authenticity':None, 'final':None}
        scores[user_id]['influence'] = influence_normed[user_id]
        scores[user_id]['interaction'] = interaction_normed[user_id]
        scores[user_id]['authenticity'] = authenticity_normed[user_id]

        # Add overall score to scores
        scores[user_id]['final'] = (0.6*influence_normed[user_id] +
                            0.3*interaction_normed[user_id] +
                            0.1*authenticity_normed[user_id])
    return scores

def find_top_influencers(G, filepath_interactions, filepath_captions):
    """
    Find top influencers based on a graph of influencers and followers,
    numbers of likes, and authenticity of posts.

    Args:
        G (nx.Graph()): Graph object, with all influencers and followers.
        filepath_interactions (str): Filepath to json with interactions dictionary.
        filepath_captions (str): Filepath to json with captions dictionary.

    Returns:
        scores (dict): Dictionary with all score types, and final scores.
    """
    # Reduce by in-degree
    G_reduced = reduce_by_critical_mass(G)
    interactions_dict = load_json(filepath_interactions)
    captions_dict = load_json(filepath_captions)

    # Calculate different scores
    influence_score = calc_community_influence_score(G_reduced, returned='dict')
    interaction_score = calc_interaction_score(G_reduced, interactions_dict, returned='dict')
    authenticity_score = calc_authenticity_score(G_reduced, captions_dict, returned='dict')

    # Calculate final scores
    scores = calc_overall_score(influence_score, interaction_score, authenticity_score)

    return scores
