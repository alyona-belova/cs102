from api import get_friends
from igraph import Graph, plot, drawing
import time
from copy import deepcopy


def get_network(user_id, as_edgelist=True):
    user_friends = get_friends(user_id, '')
    links = []
    for i, friend in enumerate(user_friends):
        friends = []
        friends = get_friends(friend, '')
        time.sleep(0.34)
        for _, friend in enumerate(friends):
            for k, another_friend in enumerate(user_friends):
                if friend == another_friend:
                    links.append((i, k))

    return links


def plot_graph(user_id):
    links = get_network(user_id)
    user_friends = get_friends(user_id, 'last_name')
    last_names = []
    for friend in user_friends:
        last_names.append(friend['last_name'])
    graph = Graph(vertex_attrs={"label": last_names, "shape": "circle", "size": 10}, edges=links, directed=False)
    N = len(last_names)
    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "layout": graph.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }
    visual_style["layout"] = graph.layout_fruchterman_reingold(
        maxiter=1000,
        area=N**2,
        repulserad=N**2)
    graph.simplify(multiple=True, loops=True)
    clusters = graph.community_multilevel()
    pal = drawing.colors.ClusterColoringPalette(len(clusters))
    graph.vs['color'] = pal.get_many(clusters.membership)
    plot(graph, **visual_style)


if __name__ == "__main__":
    plot_graph(372097810)
