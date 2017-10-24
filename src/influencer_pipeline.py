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
