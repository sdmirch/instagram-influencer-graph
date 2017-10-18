import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')


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

def plot_centralities(G, x_axis='eigenvector', y_axis='degree'):
    """
    Compare two centralities within a graph (degree, closeness, betweenness,
    eigenvector, pagerank) via plotting.

    Args:
        G (nx.Graph()): Graph object.
        x_axis (Optional[str]): Type of centrality measure to go on the x-axis.
        y_axis (Optional[str]): Type of centrality measure to go on the y-axis.

    Returns:
        plot of y_axis centrality measure v. x_axis centrality measure
    """

    x_dict = dict(nx.eigenvector_centrality(G))
    y_dict = dict(nx.degree_centrality(G))

    # Create lists of centralities matched by id
    x = []
    y = []
    for k,v in y_dict.iteritems():
        y.append(v)
        x.append(x_dict[k])

    x_line = np.linspace(0,max(max(x), max(y)),10)
    y_line = x_line

    fig, ax = plt.subplots()
    ax.plot(x, y, 'bo', alpha=0.5)
    ax.plot(x_line,y_line,'r-')
    ax.set_title("Degree Centrality v. Eigenvector Centrality")
    ax.set_xlabel("Eigenvector Centrality")
    ax.set_ylabel("Degree Centrality")
    fig.show()
