"""
Exact Minimum Vertex Cover solver using Branch-and-Bound.
"""
from graphs import getEdges

def branchbound(graph, n):
    edges = getEdges(graph)

    # start with worst-case cover
    best = [set(range(n))]

    def bb(remaining_edges, current_cover, remaining_graph):

        # base case -> all edges are covered
        if not remaining_edges:
            if len(current_cover) < len(best[0]):
                best[0] = set(current_cover)
            return

        # prune
        if len(current_cover) >= len(best[0]):
            return

        # pick the highest vertex to branch on
        bestV = max(remaining_graph, key=lambda v: len(remaining_graph[v]), default=None)

        # go back -> pick an endpoint of first remaining edge
        if bestV is None or len(remaining_graph[bestV]) == 0:
            bestV = remaining_edges[0][0]

        def removeVertex(vertex, r_edges, r_graph):
            # remove vertex and connected edges
            new = {v: set(nums) for v, nums in r_graph.items()}

            for neighbor in list(new[vertex]):
                new[neighbor].discard(vertex)

            new[vertex] = set()
            newEdges = [(u, v) for (u, v) in r_edges if u != vertex and v != vertex]
            return newEdges, new

        # branch A: include bestV
        newEdgesA, newA = removeVertex(bestV, remaining_edges, remaining_graph)
        bb(newEdgesA, current_cover | {bestV}, newA)

        # branch B: exclude bestV
        neighbors = list(remaining_graph[bestV])
        if neighbors:
            newCoverB = current_cover | set(neighbors)
            newB = {v: set(nums) for v, nums in remaining_graph.items()}
            newEdgesB = list(remaining_edges)

            for nb in neighbors:
                newEdgesB, newB = removeVertex(nb, newEdgesB, newB)
                
            bb(newEdgesB, newCoverB, newB)

    bb(edges, set(), graph)
    return best[0]