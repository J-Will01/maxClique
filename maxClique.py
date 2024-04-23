###############################################################################
# File: maxClique.py                                                           #
# Created: Friday, April 19th 2024 at 10:12:08                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Tuesday, April 23rd 2024 16:48:54                             #
# Modified By: Jonathan Williams                                               #
###############################################################################

import bruteForce
import graphComplement
import original
import genetic

import networkx as nx

import matplotlib.pyplot as plt
import time

import tkinter as tk
from tkinter import filedialog


def getFile():
    print("Use the file dialog to open a file to use:")

    # Open a file dialog for selecting a file
    root = tk.Tk()
    root.withdraw()
    filePath = filedialog.askopenfilename()

    # Check if a file was selected
    if filePath:
        print("Selected file: ", filePath)
        return filePath
        # You can do further processing with the selected file here
    else:
        return getFile()


def writeData(filePath, clique, numNodes, elapsedTime, algoUsed):
    print(f"Max Clique: {clique} of size {len(clique)}")
    print(f"Time Elapsed: {elapsedTime}s")

    with open("data.txt", "a") as file:
        file.write(
            f"{algoUsed} | {filePath} | {numNodes} | {clique} | {len(clique)} | {elapsedTime}\n"
        )


def main():

    filePath = "competition/G250.adjlist"  # getFile()

    graph = nx.Graph()
    graph: nx.Graph = nx.read_adjlist(filePath)
    # graph: nx.Graph = nx.read_edgelist(path=filePath, comments="c")

    start = time.time()
    clique = graphComplement.maxClique(graph)
    end = time.time()
    elapsedTime = round(end - start, 3)

    writeData(filePath, clique, graph.number_of_nodes(), elapsedTime, "Vertex Cover")

    return 0


if __name__ == "__main__":
    main()
