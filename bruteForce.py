###############################################################################
# File: bruteForce.py                                                          #
# Created: Sunday, April 21st 2024 at 17:56:18                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Sunday, April 21st 2024 21:41:14                              #
# Modified By: Jonathan Williams                                               #
###############################################################################

## Supplemental file to run brute force maximum clique finding in the main file
import tkinter as tk
import networkx as nx


def isClique(graph: nx.Graph, subset):
    for vertex1 in subset:
        for vertex2 in subset:
            if vertex1 != vertex2 and not graph.has_edge(str(vertex1), str(vertex2)):
                return False
    return True


def bruteforce(graph: nx.Graph):
    numNodes = graph.number_of_nodes()
    maxClique = []

    # 2^n subsets (including the empty set, so we start at 1 to avoid it)
    for subset in range(1, 2**numNodes):
        # Bitwise shifting to create unique subsets
        vertices = [v for v in range(numNodes) if subset & (1 << v)]
        if len(vertices) == 1:
            print(f"Testing Node {vertices[0]}")
        if isClique(graph, vertices) and len(vertices) > len(maxClique):
            maxClique = vertices

    return maxClique
