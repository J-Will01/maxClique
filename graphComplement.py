###############################################################################
# File: graphComplement.py                                                     #
# Created: Sunday, April 21st 2024 at 21:56:52                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Sunday, April 21st 2024 23:31:26                              #
# Modified By: Jonathan Williams                                               #
###############################################################################

## Supplemental file to run a graph complement algorithm to find a maximum clique
import networkx as nx
import matplotlib.pyplot as plt


def vertexCover(graph: nx.Graph):
    graphComplement = nx.complement(graph)
    independentSet = nx.maximal_independent_set(graphComplement)
    minVertexCover = set(graph.nodes()) - set(independentSet)
    return minVertexCover


def isClique(graph: nx.Graph, subset):
    for vertex1 in subset:
        for vertex2 in subset:
            if vertex1 != vertex2 and not graph.has_edge(str(vertex1), str(vertex2)):
                return False
    return True


# C = IS(G') = G' - VC(G')
def maxClique(graph: nx.Graph):
    complementGraph: nx.Graph = nx.complement(graph)  # G'
    vcNodeSet = vertexCover(complementGraph)  # VC(G')
    complementGraph.remove_nodes_from(vcNodeSet)  # G' - VC(G')
    print(complementGraph.nodes)
    if isClique(graph, complementGraph.nodes):
        return complementGraph.nodes
    return []
