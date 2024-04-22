###############################################################################
# File: maxClique.py                                                           #
# Created: Friday, April 19th 2024 at 10:12:08                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Sunday, April 21st 2024 20:50:47                              #
# Modified By: Jonathan Williams                                               #
###############################################################################

import bruteForce as bf
import networkx as nx

import matplotlib.pyplot as plt

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


def main():

    filePath = "G/D14G100.adjlist"  # getFile() change back for final

    graph = nx.Graph()
    graph: nx.Graph = nx.read_adjlist(filePath)

    print(f"Max Clique: {bf.bruteforce(graph)}")
    print(f"Max Clique has {len(bf.bruteforce(graph))} nodes")
    # Draw the graph
    nx.draw(graph, with_labels=True)

    plt.show()
    return 0


if __name__ == "__main__":
    main()
