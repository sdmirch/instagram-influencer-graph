import networkx as nx


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

def calc_community_influence_score(G):
    """
    Calculate and sort by community influence scores, which is eigenvector centrality
        for a graph.

    Args:
        G (nx.Graph()): Graph object.

    Returns:
        sorted_influence_score (list of tuples): List of nodes sorted by eigenvector
            centrality.
    """

    c = nx.eigenvector_centrality(G)
    sorted_influence_score = (sorted(c.iteritems(), key=lambda x: x[1], reverse=True))
    return sorted_influence_score


def calc_interaction_score(d):
    """
    Calculate and sort by interaction scores for reduced graph based
        on likes and followers.

    Args:
        d (dict): Dictionary with user ids, number of likes, and number of followers.

    Returns:
        sorted_interaction_score
    """
    interaction_score = {}

    for user_id in d.keys():
        interaction_score[user_id] = (1.0*d[user_id]['max_likes']/d[user_id]['num_follow'])

    # Add Selena Gomez for test
    interaction_score['SelenaGomez'] = 0.05

    sorted_interaction_score = (sorted(interaction_score.iteritems(), key=lambda x: x[1], reverse=True))
    return sorted_interaction_score
