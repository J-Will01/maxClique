###############################################################################
# File: graphComplement.py                                                     #
# Created: Sunday, April 21st 2024 at 21:56:52                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Wednesday, April 24th 2024 11:24:07                           #
# Modified By: Jonathan Williams                                               #
###############################################################################
## Supplemental file to run a graph complement algorithm to find a maximum clique

# Goal:
# Develop a solver that utilizes the O(E) vertex cover algorithm
# that guarentees no worse than 2x solution (for all edges, if the
# edge isn't already covered add both vertices to cover). You will
# map this back to a maximal clique via NP Hard reductions. Remember
# the independent set is G.V - VC(G)  (Vertices of G take away vertices
# of cover) and Max Clique of G' (compliment graph) is the independent
# set of G. Essentially you can find a clique by finding the VC in G'.

import random
import networkx as nx
import matplotlib.pyplot as plt


# Vertex Cover Algorithm
# Proof: This Algorithm finds in the end is a matching (a set of edges no two
# of which share an endpoint) that is “maximal” (meaning that you can’t add any
# more edges to it and keep it a matching). This means if we take both endpoints
# of those edges, we must have a vertex cover. In particular, if the algorithm
# picked k edges, the vertex cover found has size 2k. But, any vertex cover must
# have size at least k since it needs to have at least one endpoint of each of
# these edges, and since these edges don’t touch, these are k different vertices.
# So the algorithm is a 2-approximation
# From: https://www.cs.cmu.edu/~avrim/451f13/lectures/lect1105.pdf
def vertexCover(graph: nx.Graph):
    edgeList = list(graph.edges())
    cover = set()
    while edgeList:
        # Pick a random edge from remaining edges, get its vertices
        u, v = random.choice(edgeList)
        # Add vertices to the cover
        cover.add(u)
        cover.add(v)
        # Re populates edge list with all edges not incident to u and v
        edgeList = [edge for edge in edgeList if u not in edge and v not in edge]
    return cover


def isClique(graph: nx.Graph, subset):
    for vertex1 in subset:
        for vertex2 in subset:
            if vertex1 != vertex2 and not graph.has_edge(str(vertex1), str(vertex2)):
                return False
    return True


# C = IS(G') = G' - VC(G')
def maxClique(graph: nx.Graph):
    complementGraph = nx.Graph()
    bestClique = []
    minCliqueSize = 0
    failsafe = 0
    failsafeMax = 100
    while 1:
        print("Failsafe:")
        while not complementGraph.nodes or len(complementGraph.nodes) < minCliqueSize:
            complementGraph: nx.Graph = nx.complement(graph)  # G'
            vcNodeSet = vertexCover(complementGraph)  # VC(G')
            complementGraph.remove_nodes_from(vcNodeSet)  # G' - VC(G')
            if complementGraph.number_of_nodes() > len(bestClique):
                bestClique = list(complementGraph.nodes)
            failsafe += 1
            print(failsafe, end="\r")
            if failsafe == failsafeMax:
                print(failsafe)
                return bestClique
        else:
            print(failsafe)
            print("Resetting Failsafe...")
            failsafe = 0
            minCliqueSize += 1

    return complementGraph.nodes
