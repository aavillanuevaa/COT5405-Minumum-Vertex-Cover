"""
2-Approximation algorithm for Minimum Vertex Cover.

Algorithm:
  1. While there are uncovered edges:
       a. Pick any uncovered edge (u, v)
       b. Add BOTH u and v to the cover
       c. Remove all edges incident to u or v
  2. Return the cover
"""
from graphs import copyGraph

def greedy(graph):
    # work on copy 
    working = copyGraph(graph)
    cover = set()

    while True:
        # find remaining uncovered edges
        edge = pickEdge(working)

        # all edges covered
        if edge is None:
            break

        u, v = edge

        # add both endpoints to cover
        cover.add(u)
        cover.add(v)

        # remove all edges connected to u and v
        removeVertex(u, working)
        removeVertex(v, working)

    return cover

def pickEdge(graph):
    # return first edge found
    # returns None if no edges remain
    for u in graph:
        if graph[u]:
            v = next(iter(graph[u]))
            return (u, v)
    return None

def removeVertex(vertex, graph):
    # remove all edges connected to vertex
    for neighbor in list(graph[vertex]):
        graph[neighbor].discard(vertex)
    graph[vertex] = set()
