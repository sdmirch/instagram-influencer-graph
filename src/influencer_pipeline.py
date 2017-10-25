import networkx as nx
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def reduce_by_critical_mass(G, crit_mass=5000):
    """
    Reduces graph by removing nodes that have less than a specific number of
        followers (critical mass).

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
