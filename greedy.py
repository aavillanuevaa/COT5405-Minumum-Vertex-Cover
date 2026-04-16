"""
greedy.py
---------
2-Approximation algorithm for Minimum Vertex Cover.

Technique : Greedy Approximation
Worst-case: O(V+E)
Type      : Approximation — guarantees cover size <= 2 * OPT

Based on the approach described in:
  https://www.geeksforgeeks.org/dsa/introduction-and-approximate-solution-for-vertex-cover-problem/

Algorithm:
  1. While there are uncovered edges:
       a. Pick any uncovered edge (u, v)
       b. Add BOTH u and v to the cover
       c. Remove all edges incident to u or v
  2. Return the cover
"""

from graphs import graph_copy


def greedy_vertex_cover(graph):
    # work on a copy so the original graph is not modified
    working_graph = graph_copy(graph)
    cover = set()

    while True:
        # find any remaining uncovered edge
        edge = pick_edge(working_graph)

        # all edges are covered
        if edge is None:
            break

        u, v = edge

        # add both endpoints to the cover
        cover.add(u)
        cover.add(v)

        # remove all edges incident to u and v
        remove_vertex(u, working_graph)
        remove_vertex(v, working_graph)

    return cover

# --- helpers ---------------------------------------------------- #

def pick_edge(graph):
    # scan adjacency list and return the first edge found
    # returns None if no edges remain
    for u in graph:
        if graph[u]:
            v = next(iter(graph[u]))
            return (u, v)
    return None


def remove_vertex(vertex, graph):
    # remove all edges incident to vertex
    for neighbor in list(graph[vertex]):
        graph[neighbor].discard(vertex)
    graph[vertex] = set()
