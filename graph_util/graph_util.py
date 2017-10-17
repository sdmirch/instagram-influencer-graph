import networkx as nx



def compare_centralities(G, top=5):
    """
    Compare centralities within a graph: degree, closeness, betweenness,
    eigenvector, page-rank.

    Args:
        G (nx.Graph()): Graph object.
        top (Optional[int]): Top nodes for centrality measures, default 5.

    Returns:
        most_important (set): Most important nodes for all centrality measures.
    """
    most_important = set()

    d = nx.degree_centrality(G)
    c = nx.closeness_centrality(G)
    b = nx.betweenness_centrality(G)
    e = nx.eigenvector_centrality(G)
    p = nx.pagerank(G)

    centralities = [d, c, b, e, p]
    names = ['degree','closeness','betweenness','eigenvector','page-rank']

    for i, centrality in enumerate(centralities):
        sorted_centrality = (sorted(centrality.iteritems(), key=lambda x: x[1], reverse=True))[:top]
        print names[i]
        print sorted_centrality
        print "\n"

        for pair in sorted_centrality:
            most_important.add(pair[0])

    return most_important
