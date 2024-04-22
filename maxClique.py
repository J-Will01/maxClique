###############################################################################
# File: maxClique.py                                                           #
# Created: Friday, April 19th 2024 at 10:12:08                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Sunday, April 21st 2024 22:24:59                              #
# Modified By: Jonathan Williams                                               #
###############################################################################

import bruteForce
import graphComplement

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

    filePath = "G/D14G100.adjlist"  # getFile() change back for final

    graph = nx.Graph()
    graph: nx.Graph = nx.read_adjlist(filePath)

    start = time.time()
    clique = graphComplement.maxClique(graph)
    end = time.time()
    elapsedTime = round(end - start, 3)

    print(f"Max Clique: {clique} of size {len(clique)}")
    print(f"Time Elapsed: {elapsedTime}s")
    # writeData(filePath, clique, graph.number_of_nodes(), elapsedTime, "Brute Force")

    # Draw the graph
    # nx.draw(graph, with_labels=True)
    # plt.show()

    return 0


if __name__ == "__main__":
    main()
