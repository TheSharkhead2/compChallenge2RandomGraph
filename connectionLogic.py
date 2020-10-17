import random 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt

def display_graph_ranked(nodesColor, adjMatrix): #temp
    G = nx.DiGraph()
    G.add_nodes_from(list(range(len(nodesColor))))
    
    edgeValues = {}
    edges = []
    rowIndex = 0
    for row in adjMatrix:
        edgeIndex = 0
        for edge in row:
            if edge != 0: #look for edge between two nodes and make sure that "duplicate" of edge not already accounted for
                edges.append((rowIndex, edgeIndex))
                edgeValues[(rowIndex, edgeIndex)] = edge
            edgeIndex += 1
        rowIndex += 1
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=nodesColor, edge_color='black',width=1,linewidths=1)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edgeValues, font_size=4) #citation: https://stackoverflow.com/questions/47094949/labeling-edges-in-network
    plt.axis('off')
    plt.show()

def check_can_connect(endingNodeIndex, adjMatrix):
    for edge in adjMatrix[endingNodeIndex]:
        if edge == 1:
            # print("{} is bad".format(endingNodeIndex))
            return(False)
    # print("{} is GOOD".format(endingNodeIndex))
    return(True)

def choose_connection(nodeIndex, nodeColor, nodesScore, adjMatrix): #used for initial random assignment
    if not check_can_connect(nodeIndex, adjMatrix):
        return(adjMatrix)
    nNodes = len(nodesScore)
    possibleConnections = [n for n in list(range(nNodes)) if check_can_connect(n, adjMatrix) and n != nodeIndex]
    
    preferedConnection = random.choice(possibleConnections)
    adjMatrix[nodeIndex][preferedConnection] = 1 
    adjMatrix[preferedConnection][nodeIndex] = 1
    return(adjMatrix)

def assignConnections(nodeList, adjMatrix, nodesScore): #used for initial random assignment
    adjMatrix = np.zeros([len(nodeList), len(nodeList)])
    index = 0
    for node in nodeList:
        adjMatrix = choose_connection(index, node, nodesScore, adjMatrix)
        index += 1
    return(adjMatrix)

def rank_choices(nodeColor, nodeIndex, nodesScore, roundNumber):
    scoredNodes = []
    nNodes = len(nodesScore)
    if nodeColor == 'red':
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            avgScore = currentScore/roundNumber #could also look at average over last 5 rounds or something 
            
            assignedScore = random.random() #random selection
            scoredNodes.append((index, assignedScore))

    elif nodeColor == 'green':
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            avgScore = currentScore/roundNumber #could also look at average over last 5 rounds or something 
            
            assignedScore = random.random() #random selection
            scoredNodes.append((index, assignedScore))

    elif nodeColor == "blue":
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            avgScore = currentScore/roundNumber #could also look at average over last 5 rounds or something 
            
            assignedScore = random.random() #random selection
            scoredNodes.append((index, assignedScore))

    scoredNodesRanked = sorted(scoredNodes, reverse=True, key=lambda score: score[1]) #citation: https://docs.python.org/3/howto/sorting.html
    rankedChoices = [score[0] for score in scoredNodesRanked]
    return(rankedChoices)

def average_rank_sum(adjMatrix, preferenceAdjMatrixValues):
    sumRanks = []
    edges = []
    rowIndex = 0
    for row in adjMatrix:
        edgeIndex = 0
        for edge in row:
            if edge == 1 and (edgeIndex, rowIndex) not in edges: #look for edge between two nodes and make sure that "duplicate" of edge not already accounted for
                edges.append((rowIndex, edgeIndex))
            edgeIndex += 1
        rowIndex += 1
    
    for edge in edges:
        sumRanks.append(preferenceAdjMatrixValues[edge[0]][edge[1]] + preferenceAdjMatrixValues[edge[1]][edge[0]])
    
    return(sum(sumRanks)/len(sumRanks))

def create_connections(nodesColor, nodesScore, roundNumber, adjMatrix):
    nodesRankedChoice = []
    nNodes = len(nodesScore)
    
    for index in range(nNodes):
        nodesRankedChoice.append(rank_choices(nodesColor[index], index, nodesScore, roundNumber))
    preferenceAdjMatrixValues = np.zeros([nNodes, nNodes])
    preferenceAdjMatrix = np.zeros([nNodes, nNodes])
    for index, rankedChoices in zip(list(range(nNodes)), nodesRankedChoice):
        for conNodeIndex, rank in zip(rankedChoices, list(range(len(rankedChoices)))):

            preferenceAdjMatrixValues[index][conNodeIndex] = rank + 1
            preferenceAdjMatrix[index][conNodeIndex] = 1
    
    print(preferenceAdjMatrixValues)
    adjMatrix = assignConnections(nodesColor, adjMatrix, nodesScore)

    for rankCutoff in range(nNodes):
        rankCutoff += 1 
        preferenceAdjMatrixValuesCuttoff = np.copy(preferenceAdjMatrixValues) 
        preferenceAdjMatrixCuttoff = np.copy(preferenceAdjMatrix)
        for row, rowIndex in zip(preferenceAdjMatrixValuesCuttoff, list(range(np.shape(preferenceAdjMatrixValuesCuttoff)[0]))):
            for value, valueIndex in zip(row, list(range(np.shape(preferenceAdjMatrixValuesCuttoff)[1]))):
                if value > rankCutoff:
                    preferenceAdjMatrixCuttoff[rowIndex][valueIndex] = 0 
                    preferenceAdjMatrixValuesCuttoff[rowIndex][valueIndex] = 0

        walksLen2 = np.linalg.matrix_power(preferenceAdjMatrixCuttoff, 2)
        for pair, index in zip(np.diag(walksLen2), list(range(len(np.diag(walksLen2))))):
            if pair > 0:
                print(pair) #for testing purposes 
                print(index) #for testing purposes

                testAdjMatrix = np.copy(adjMatrix)

                for tempEdge, tempConIndex in zip(preferenceAdjMatrixCuttoff[index], list(range((len(preferenceAdjMatrixCuttoff[index]))))):
                    if tempEdge == 1 and preferenceAdjMatrixCuttoff[tempConIndex][index] == 1:
                        testAdjMatrix[index][tempConIndex] = 1 #here need to make sure to remove edge to other node that each is connected to 
                        testAdjMatrix[tempConIndex][index] = 1
                        break

                
                
                if average_rank_sum(testAdjMatrix, preferenceAdjMatrixValues) > average_rank_sum(adjMatrix, preferenceAdjMatrixValues):
                    adjMatrix = testAdjMatrix


