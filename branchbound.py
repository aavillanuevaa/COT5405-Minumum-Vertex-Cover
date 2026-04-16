"""
Exact Minimum Vertex Cover solver using Branch-and-Bound.

Technique : Branch-and-Bound (Exact Exponential Algorithm)
Worst-case: O(2^n)
Type      : Exact solution (always finds the true minimum vertex cover)

Based on the approach described in:
  https://www.mdpi.com/2227-7390/7/7/603
"""

from graphs import get_edges


def branchbound(graph, n):
    edges = get_edges(graph)

    # start with the trivial worst-case cover (all vertices)
    best_cover = [set(range(n))]

    def bb(remaining_edges, current_cover, remaining_graph):

        # base case: all edges are covered
        if not remaining_edges:
            if len(current_cover) < len(best_cover[0]):
                best_cover[0] = set(current_cover)
            return

        # prune: current cover is already as large as the best found
        if len(current_cover) >= len(best_cover[0]):
            return

        # pick the highest-degree vertex to branch on
        best_vertex = max(remaining_graph,
                          key=lambda v: len(remaining_graph[v]),
                          default=None)

        # fallback: pick an endpoint of the first remaining edge
        if best_vertex is None or len(remaining_graph[best_vertex]) == 0:
            best_vertex = remaining_edges[0][0]

        def remove_vertex(vertex, r_edges, r_graph):
            # remove vertex and all its incident edges
            new_graph = {v: set(nbrs) for v, nbrs in r_graph.items()}
            for neighbor in list(new_graph[vertex]):
                new_graph[neighbor].discard(vertex)
            new_graph[vertex] = set()
            new_edges = [(u, v) for (u, v) in r_edges
                         if u != vertex and v != vertex]
            return new_edges, new_graph

        # branch A: include best_vertex in the cover
        new_edges_a, new_graph_a = remove_vertex(best_vertex,
                                                 remaining_edges,
                                                 remaining_graph)
        bb(new_edges_a, current_cover | {best_vertex}, new_graph_a)

        # branch B: exclude best_vertex, so all its neighbors must be included
        neighbors = list(remaining_graph[best_vertex])
        if neighbors:
            new_cover_b = current_cover | set(neighbors)
            new_graph_b = {v: set(nbrs) for v, nbrs in remaining_graph.items()}
            new_edges_b = list(remaining_edges)
            for nb in neighbors:
                new_edges_b, new_graph_b = remove_vertex(nb,
                                                         new_edges_b,
                                                         new_graph_b)
            bb(new_edges_b, new_cover_b, new_graph_b)

    bb(edges, set(), graph)
    return best_cover[0]
