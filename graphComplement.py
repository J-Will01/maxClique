###############################################################################
# File: graphComplement.py                                                     #
# Created: Sunday, April 21st 2024 at 21:56:52                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Sunday, April 21st 2024 22:37:09                              #
# Modified By: Jonathan Williams                                               #
###############################################################################

## Supplemental file to run a graph complement algorithm to find a maximum clique
import networkx as nx


# C = IS(G') = G' - VC(G')
def maxClique(graph: nx.Graph):

    maxClique = []
    complementGraph: nx.Graph = nx.complement(graph)  # G'
    verrtexCover = nx.min_edge_cover(complementGraph)  # VC(G')
    complementGraph.remove_nodes_from(verrtexCover)  # G' - VC(G')

    # Print the nodes and edges of the result graph
    print("Nodes in result graph:", complementGraph.nodes())
    print("Edges in result graph:", complementGraph.edges())

    return maxClique
