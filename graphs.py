"""
Random graph generation utilities.
Used by both algorithm modules and experiments.py.
"""
import random

def generateRandomGraph(n, p, seed=None):  
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


def copyGraph(graph):
    # return a copy of graph
    return {v: set(neighbors) for v, neighbors in graph.items()}

def getEdges(graph):
    # extract all edges 
    edges = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.append((u, v))
    return edges

def verifyVertexCover(cover, edges):
    # check every edge has at least one endpoint in cover
    for u, v in edges:
        if u not in cover and v not in cover:
            return False
    return True
