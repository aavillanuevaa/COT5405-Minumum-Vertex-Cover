"""
Random graph generation utilities.
Used by both algorithm modules and experiments.py.
"""

import random


def generate_random_graph(n, p, seed=None):
    """
    Generate a random undirected graph using the Erdos-Renyi G(n, p) model.

    Parameters:
        n    (int)   : number of vertices (labeled 0 to n-1)
        p    (float) : probability that any given edge exists (0.0 to 1.0)
        seed (int)   : optional random seed for reproducibility

    Returns:
        graph (dict) : adjacency list {vertex: set of neighbors}
        edges (list) : list of all edges as (u, v) tuples with u < v
    """
    if seed is not None:
        random.seed(seed)

    # initialize empty adjacency list for every vertex
    graph = {i: set() for i in range(n)}
    edges = []

    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                graph[u].add(v)
                graph[v].add(u)
                edges.append((u, v))

    return graph, edges


def graph_copy(graph):
    # return a deep copy of an adjacency-list graph
    return {v: set(neighbors) for v, neighbors in graph.items()}


def get_edges(graph):
    # extract all edges from an adjacency list (each edge returned once)
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.append((u, v))
    return edges


def verify_vertex_cover(cover, edges):
    # check that every edge has at least one endpoint in the cover
    for u, v in edges:
        if u not in cover and v not in cover:
            return False
    return True
