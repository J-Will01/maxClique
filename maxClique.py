###############################################################################
# File: maxClique.py                                                           #
# Created: Friday, April 19th 2024 at 10:12:08                                 #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Wednesday, April 24th 2024 12:54:40                           #
# Modified By: Jonathan Williams                                               #
###############################################################################

import sys
import bruteForce
import graphComplement
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


def quit():
    root.destroy()  # Close the main window
    sys.exit()


def brute():
    start = time.time()
    clique = bruteForce.maxClique(graph)
    end = time.time()
    elapsedTime = round(end - start, 3)

    writeData(filePath, clique, graph.number_of_nodes(), elapsedTime, "Brute Force")


def vertex():
    start = time.time()
    clique = graphComplement.maxClique(graph)
    end = time.time()
    elapsedTime = round(end - start, 3)

    writeData(filePath, clique, graph.number_of_nodes(), elapsedTime, "Vertex Cover")


def original():
    start = time.time()
    clique = genetic.maxClique(graph)
    end = time.time()
    elapsedTime = round(end - start, 3)

    writeData(filePath, clique, graph.number_of_nodes(), elapsedTime, "Original GA")


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Algorithm Menu")

    # Calculate the position to center the window
    screenX = root.winfo_screenwidth()
    screenY = root.winfo_screenheight()
    xPos = (screenX - 200) // 2
    yPos = (screenY - 200) // 2
    root.geometry(f"200x200+{xPos}+{yPos}")

    # Get File for input
    filePath = getFile()

    # Get graph from file
    graph: nx.Graph = nx.read_adjlist(filePath)

    # Add label for instructions
    lbl_instructions = tk.Label(root, text="Select an Algorithm:")
    lbl_instructions.pack()

    # Create the menu buttons
    btn_algorithm_1 = tk.Button(root, text="Brute Force", command=brute)
    btn_algorithm_1.pack()

    btn_algorithm_2 = tk.Button(root, text="Vertex Cover", command=vertex)
    btn_algorithm_2.pack()

    btn_algorithm_3 = tk.Button(root, text="Original GA", command=original)
    btn_algorithm_3.pack()

    btn_quit = tk.Button(root, text="Quit", command=quit)
    btn_quit.pack()

    # Run the main event loop
    root.mainloop()
