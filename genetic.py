###############################################################################
# File: genetic.py                                                             #
# Created: Monday, April 22nd 2024 at 9:20:7                                   #
# Author: Jonathan Williams                                                    #
# -----                                                                        #
# Last Modified: Thursday, April 25th 2024 13:23:40                            #
# Modified By: Jonathan Williams                                               #
###############################################################################

# Input: G = (V, E)
# Output: A maximal clique in G
# 1. Preprocess the input graph
# 2. Create an initial population
# 3. Apply the local optimization to each chromosome
# 4. while (stopping condition is not met) do
# 5. Select two parents, P1 and P2, from the population
# 6. Generate two offspring by crossing over P1 and P2
# 7. Mutate the two offspring
# 8. Local optimize the two offspring
# 9. Replace a population member with a better offspring
# 10. Update stopping condition
# 11. return the best member of the population


# Imports
from matplotlib import pyplot as plt
import networkx as nx
import random

# GA Constants
STAGNANCY = 50
INITIAL_POPULATION = 100
SELECTION_PROB = 0.7
MUTATION_PROB = 0.4
CUTS = 10
GENS_CUT_REDUCTION = 20


def preprocess(graph):
    # degrees = dict(graph.degree())
    # sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    # mapping = {vertex: rank for rank, (vertex, _) in enumerate(sorted_nodes)}
    # reordered_graph = nx.relabel_nodes(graph, mapping)
    mapping = {node: i for i, node in enumerate(graph.nodes())}
    newGraph = nx.relabel_nodes(graph, mapping)
    return newGraph


def subgraphToChromosome(graph: nx.Graph, subgraph: nx.Graph):
    chromosome = [1 if node in subgraph.nodes else 0 for node in graph.nodes]
    return chromosome


def chromosomeToClique(chromosome: list):
    clique = [i for i, gene in enumerate(chromosome) if gene == 1]
    return clique


def initialPopulation(graph: nx.Graph):
    population = []
    popSize = INITIAL_POPULATION

    while len(population) < popSize:
        subset = []
        usedNeighbors = set()

        # Randomly select a vertex
        randomVertex = random.choice(list(graph.nodes))
        subset.append(randomVertex)

        while len(usedNeighbors) < len(set(graph.neighbors(randomVertex))):
            feasible_neighbors = [
                neighbor
                for neighbor in graph.neighbors(randomVertex)
                if neighbor not in usedNeighbors
            ]
            if not feasible_neighbors:
                break
            # Randomly choose a feasible neighbor
            neighbor = random.choice(feasible_neighbors)

            # Add vert to used vertices
            usedNeighbors.add(neighbor)

            # Check if adding the neighbor maintains the clique property
            if all(node in graph.neighbors(neighbor) for node in subset):
                subset.append(neighbor)
            else:
                continue

        # Convert subset to chromosome
        chromosome = [1 if node in subset else 0 for node in graph.nodes]
        population.append(chromosome)

    population = mutatePopulation(population, SELECTION_PROB, MUTATION_PROB)
    for i in range(len(population)):
        population[i] = optimizeChromosome(population[i], graph)

    return population


def initialFitness(population: list):
    fitnessVals = []
    for chromosome in population:

        fitnessVals.append(getFitness(chromosome))
    return fitnessVals


def mutatePopulation(population, selectionProbability, mutationProbability):
    mutatedPop = []
    for chromosome in population:
        # Choose chromosome to mutate based on selection probability
        mutatedPop.append(
            mutateChromosome(chromosome, selectionProbability, mutationProbability)
        )

    return mutatedPop


def mutateChromosome(chromosome: list, selectionProbability, mutationProbability):
    if random.random() <= selectionProbability:
        mutatedChromosome = []
        for gene in chromosome:
            # Mutate each gene according to mutation probability
            if random.random() <= mutationProbability:
                mutatedGene = 1 - gene  # Flip the bit (0 to 1 or 1 to 0)
            else:
                mutatedGene = gene
            mutatedChromosome.append(mutatedGene)
        return mutatedChromosome
    return chromosome


# Get fitness in the form of clique size
def getFitness(chromosome):
    return sum(chromosome)


# Normalize fitness to a range of 0 to 1, for parent selction
def normalizeFitness(fitnessVals):
    minFit = min(fitnessVals)
    maxFit = max(fitnessVals)
    fitRange = maxFit - minFit
    # Handle fit range of zero
    if fitRange == 0:
        return [0.5] * len(fitnessVals)
    # Scaled 0.1 to 0.9 to prevent hard 0 - 1 fitnessvals for small clique sizes
    normalizedFitnessVals = [
        float(fitness - minFit) / float(fitRange) * (0.9 - 0.1) + 0.1
        for fitness in fitnessVals
    ]
    return normalizedFitnessVals


def crossover(parent1, parent2, numCrossovers):
    # Multi point crossover
    child1 = []
    child2 = []

    lastCut = 0
    cutPoints = sorted(random.sample(range(1, len(parent1)), numCrossovers))
    cutPoints.append(len(parent1))  # Fix short chromosome children

    for point in cutPoints:
        if (lastCut % 2) == 0:
            child1.extend(parent1[lastCut:point])
            child2.extend(parent2[lastCut:point])
        else:
            child1.extend(parent2[lastCut:point])
            child2.extend(parent1[lastCut:point])
        lastCut = point

    return child1, child2


def optimizeChromosome(chromosome, graph):
    optimizedChromosome = cliqueExtraction(chromosome, graph)
    optimizedChromosome = cliqueImprovement(optimizedChromosome, graph)
    return optimizedChromosome


def cliqueImprovement(chromosome: list, graph: nx.Graph):
    clique = chromosomeToClique(chromosome)

    # Pick a random gene as the pivot
    pos = random.randint(0, len(chromosome) - 1)

    # From pivot to end
    for gene in range(pos, len(chromosome)):
        if chromosome[gene] == 0 and all(graph.has_edge(gene, node) for node in clique):
            clique.append(gene)

    # From beginning to pivot
    for gene in range(0, pos):
        if chromosome[gene] == 0 and all(graph.has_edge(gene, node) for node in clique):
            clique.append(gene)

    # Clique to chromosome again
    improvedChromosome = [1 if i in clique else 0 for i in range(len(chromosome))]

    return improvedChromosome


def getParents(population: list, fitnessVals: list):

    parents = []
    normalizedFitness = normalizeFitness(fitnessVals)

    # Get two parents through roulete style selection
    for _ in range(2):
        selection = random.uniform(0, 1)
        totalProb = 0
        for i, prob in enumerate(normalizedFitness):
            totalProb += prob
            if selection <= totalProb:
                parents.append(population[i])
                break

    return parents


def getChildren(graph: nx.Graph, parents: list, numCuts: int):
    children = [list(), list()]
    children[0], children[1] = crossover(parents[0], parents[1], numCuts)
    for i in range(0, 2):
        children[i] = mutateChromosome(children[i], SELECTION_PROB, MUTATION_PROB)
        children[i] = optimizeChromosome(children[i], graph)
    return children


def isClique(subgraph: nx.Graph):
    for node1 in subgraph.nodes():
        for node2 in subgraph.nodes():
            if node1 != node2 and not subgraph.has_edge(node1, node2):
                return False
    return True


def cliqueExtraction(chromosome: list, graph: nx.Graph):
    subgraphNodes = [i for i, bit in enumerate(chromosome) if bit == 1]
    subgraph = nx.Graph()
    subgraph: nx.Graph = graph.subgraph(subgraphNodes).copy()

    while not isClique(subgraph):
        degrees = sorted(
            [(node, subgraph.degree[node]) for node in subgraph.nodes()],
            key=lambda x: x[1],  # sort with the degree part of the tuple
        )
        minDegree = degrees[0][1]
        secondMinDegree = degrees[1][1] if len(degrees) > 1 else minDegree
        candidateNodes = [
            nodeTuple[0]
            for nodeTuple in degrees
            if nodeTuple[1] == minDegree or nodeTuple[1] == secondMinDegree
        ]

        zeroDegreeNodes = [
            node for node in subgraph.nodes() if subgraph.degree[node] == 0
        ]

        # Randomly delete a vertex, deleting zero degree nodes first if they exist
        if zeroDegreeNodes:
            vertexToRemove = random.choice(zeroDegreeNodes)
        else:
            vertexToRemove = random.choice(candidateNodes)
        subgraph.remove_node(vertexToRemove)

    chromosome = subgraphToChromosome(graph, subgraph)

    return chromosome


# Compare hamming distance of chromosomes based on number of similar genes
def hammingDist(chromosome1, chromosome2):
    return sum(gene1 != gene2 for gene1, gene2 in zip(chromosome1, chromosome2))


# Replace members of the population with more fit children
def replacement(parents: list, children: list, population: list, fitnessVals: list):
    # Take the better child
    bestChild = []
    if getFitness(children[0]) > getFitness(children[1]):
        bestChild = children[0]
    else:
        bestChild = children[1]

    bestChildFit = getFitness(bestChild)

    # Check if the child is better than either parent
    # Find more similar parent
    closeParent = []
    farParent = []
    if hammingDist(parents[0], bestChild) < hammingDist(parents[1], bestChild):
        closeParent = parents[0]
        farParent = parents[1]
    else:
        closeParent = parents[1]
        farParent = parents[0]

    # Replace parents if child is more fit
    if bestChildFit > getFitness(closeParent):
        newPos = population.index(closeParent)
        fitnessVals[newPos] = bestChildFit
        population[newPos] = bestChild
    elif bestChildFit > getFitness(farParent):
        newPos = population.index(farParent)
        fitnessVals[newPos] = bestChildFit
        population[newPos] = bestChild
    # Otherwise replace the weakest member in the population
    else:
        newPos = fitnessVals.index(min(fitnessVals))
        population[newPos] = bestChild
        fitnessVals[newPos] = bestChildFit


# Get total fitness of the population
def getPopulationFitness(population: list):
    totalFitness = 0
    for chromosome in population:
        totalFitness += getFitness(chromosome)
    return totalFitness


def maxClique(graph):
    # Preprocessing
    graph = preprocess(graph)

    # Initial population
    print("Initializing Population...")
    population = initialPopulation(graph)
    print("Initializing Fitness...")
    fitnessVals = initialFitness(population)

    stagnancy = 0
    bestGenFit = 0
    generation = 0
    cuts = CUTS

    # Genetic algorithm iterations
    while stagnancy != STAGNANCY:
        if generation % GENS_CUT_REDUCTION == 0 and cuts > 2 and generation != 0:
            cuts -= 2
        print(f"Generation: {generation}, Best Gen Fit: {bestGenFit}, Cuts: {cuts}")
        # Parent selection
        parents = getParents(population, fitnessVals)
        # Crossover, mutate, and optimize children
        children = getChildren(graph, parents, CUTS)
        # Replace parent with offspring
        replacement(parents, children, population, fitnessVals)

        if getPopulationFitness(population) <= bestGenFit:
            stagnancy += 1
        else:
            bestGenFit = getPopulationFitness(population)
            stagnancy = 0

        generation += 1

    # Find best chromosome in final population
    bestChromosomePos = fitnessVals.index(max(fitnessVals))
    bestChromosome = population[bestChromosomePos]
    clique = chromosomeToClique(bestChromosome)

    return clique
