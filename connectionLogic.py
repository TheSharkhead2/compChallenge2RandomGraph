import random 
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt

def display_graph_ranked(nodesColor, adjMatrix): 
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

def check_can_connect(endingNodeIndex, adjMatrix): #used for initial random assignment --> checks to see if one node is open to an edge (ie doesn't currently have another node adjacent to it)
    for edge in adjMatrix[endingNodeIndex]:
        if edge == 1:
            # print("{} is bad".format(endingNodeIndex))
            return(False)
    # print("{} is GOOD".format(endingNodeIndex))
    return(True)

def choose_connection(nodeIndex, nodeColor, nodesScore, adjMatrix): #used for initial random assignment --> creates list of possible connections for a node and randomly chooses one to connect to
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

def rank_choices(nodeColor, nodeIndex, nodesScore, roundNumber, rstrat='ran', gstrat='ran', bstrat='ran'): #function ranks all other nodes in terms of preference, can rank in different ways
    scoredNodes = []
    nNodes = len(nodesScore)
    avgNodeScores = [curScore/roundNumber for curScore in nodesScore] #calculate average score of nodes per round
    if nodeColor == 'red': #look at every node and assign a score to all of them in order to create ranking... same process for red, green, and blue but divided into different if statements 
        for index in list(range(nNodes)): 
            currentScore = nodesScore[index] 
            avgScore = avgNodeScores[index]

            if rstrat == 'ran': #randomly assign scores to nodes for random selection 
                assignedScore = random.random() 
            elif rstrat == 'hoscore': #prefer nodes with a higher total score
                if max(nodesScore) == 0: #if the max of score is 0, than everything is 0 so you will get divide by zero error, just avoid this (this means that first round it is just sorted randomly)
                    assignedScore = 0 
                else: 
                    assignedScore = currentScore/max(nodesScore)
            elif rstrat == 'hprscore': #prefer nodes with a higher average score per round
                if max(avgNodeScores) == 0:
                    assignedScore = 0 
                else: 
                    assignedScore = avgScore/max(avgNodeScores)
            elif rstrat == 'loscore':
                if max(nodesScore) == 0 or avgScore == 0:
                    assignedScore = 0
                else: 
                    assignedScore = max(nodesScore)/currentScore
            elif rstrat == 'lprscore':
                if max(nodesScore) == 0 or avgScore == 0:
                    assignedScore = 0
                else: 
                    assignedScore = max(avgNodeScores)/avgScore
            elif rstrat == 'moscore':
                assignedScore = (-1 * 1/((max(nodesScore) + min(nodesScore))/2)) * abs(currentScore - (max(nodesScore) + min(nodesScore))/2) + 1
            elif rstrat == 'mprscore':
                assignedScore = (-1 * 1/((max(avgNodeScores) + min(avgNodeScores))/2)) * abs(avgScore - (max(avgNodeScores) + min(avgNodeScores))/2) + 1

            if index == nodeIndex:
                assignedScore = 0 #set own score to 0 (to avoid issues later, however the program simply forgets about itself later anyway so this isn't strictly necessary)
            
            scoredNodes.append((index, assignedScore))

    elif nodeColor == 'green':
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            avgScore = avgNodeScores[index]

            if gstrat == 'ran':
                assignedScore = random.random() 
            elif gstrat == 'hoscore': 
                if max(nodesScore) == 0: 
                    assignedScore = 0 
                else: 
                    assignedScore = currentScore/max(nodesScore)
            elif gstrat == 'hprscore': 
                if max(avgNodeScores) == 0:
                    assignedScore = 0 
                else: 
                    assignedScore = avgScore/max(avgNodeScores)
            elif gstrat == 'loscore':
                if max(nodesScore) == 0 or avgScore == 0:
                    assignedScore = 0
                else: 
                    assignedScore = max(nodesScore)/currentScore
            elif gstrat == 'lprscore':
                if max(nodesScore) == 0 or avgScore == 0:
                    assignedScore = 0
                else: 
                    assignedScore = max(avgNodeScores)/avgScore
            elif gstrat == 'moscore':
                assignedScore = (-1 * 1/((max(nodesScore) + min(nodesScore))/2)) * abs(currentScore - (max(nodesScore) + min(nodesScore))/2) + 1
            elif gstrat == 'mprscore':
                assignedScore = (-1 * 1/((max(avgNodeScores) + min(avgNodeScores))/2)) * abs(avgScore - (max(avgNodeScores) + min(avgNodeScores))/2) + 1

            if index == nodeIndex:
                assignedScore = 0
            scoredNodes.append((index, assignedScore))

    elif nodeColor == "blue":
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            avgScore = avgNodeScores[index]
            
            if bstrat == 'ran':
                assignedScore = random.random() 
            elif bstrat == 'hoscore': 
                if max(nodesScore) == 0: 
                    assignedScore = 0 
                else: 
                    assignedScore = currentScore/max(nodesScore)
            elif bstrat == 'hprscore': 
                if max(avgNodeScores) == 0:
                    assignedScore = 0 
                else: 
                    assignedScore = avgScore/max(avgNodeScores)
            elif bstrat == 'loscore':
                if max(nodesScore) == 0 or avgScore == 0:
                    assignedScore = 0
                else: 
                    assignedScore = max(nodesScore)/currentScore
            elif bstrat == 'lprscore':
                if max(nodesScore) == 0 or avgScore == 0:
                    assignedScore = 0
                else: 
                    assignedScore = max(avgNodeScores)/avgScore
            elif bstrat == 'moscore':
                assignedScore = (-1 * 1/((max(nodesScore) + min(nodesScore))/2)) * abs(currentScore - (max(nodesScore) + min(nodesScore))/2) + 1
            elif bstrat == 'mprscore':
                assignedScore = (-1 * 1/((max(avgNodeScores) + min(avgNodeScores))/2)) * abs(avgScore - (max(avgNodeScores) + min(avgNodeScores))/2) + 1

            if index == nodeIndex:
                assignedScore = 0 
            scoredNodes.append((index, assignedScore))

    scoredNodesRanked = sorted(scoredNodes, reverse=True, key=lambda score: score[1]) #order scored nodes, citation: https://docs.python.org/3/howto/sorting.html
    rankedChoices = [score[0] for score in scoredNodesRanked] #pulls out ordered list of node indexes instead of tuple with score as well, something not important to the rest of the program 
    return(rankedChoices)

def average_rank_sum(adjMatrix, preferenceAdjMatrixValues): #function sums the two ranks of each pairing (so if one node ranked the other as 3 and the other ranked it as 4, this would be 7) then averages this for the whole network. This is used as placement for the "quality" of all the pairings
    sumRanks = [] 
    edges = []
    rowIndex = 0
    for row in adjMatrix: #record list of all pairings in network
        edgeIndex = 0
        for edge in row:
            if edge == 1 and (edgeIndex, rowIndex) not in edges: #look for edge between two nodes and make sure that "duplicate" of edge not already accounted for
                edges.append((rowIndex, edgeIndex))
            edgeIndex += 1
        rowIndex += 1
    
    for edge in edges:
        sumRanks.append(preferenceAdjMatrixValues[edge[0]][edge[1]] + preferenceAdjMatrixValues[edge[1]][edge[0]]) #find sum of all pairing ranks 
    
    return(sum(sumRanks)/len(sumRanks)) #return average

def create_connections(nodesColor, nodesScore, roundNumber, adjMatrix, rstrat='ran', gstrat='ran', bstrat='ran'): #function to create pairings, attempting to optimize for ranked choices of each node 
    nodesRankedChoice = []
    nNodes = len(nodesScore)
    
    for index in range(nNodes): #get the ranks for all other nodes from each node
        nodesRankedChoice.append(rank_choices(nodesColor[index], index, nodesScore, roundNumber, rstrat=rstrat, gstrat=gstrat, bstrat=bstrat))

    preferenceAdjMatrixValues = np.zeros([nNodes, nNodes])
    preferenceAdjMatrix = np.zeros([nNodes, nNodes])
    for index, rankedChoices in zip(list(range(nNodes)), nodesRankedChoice): #transfer rankings to "adjacency matrix" (one with weights and one without... though one without could probably better been generated through just a matrix of 1s with the diagonal 0 (as this ignores itself as a node))
        for conNodeIndex, rank in zip(rankedChoices, list(range(len(rankedChoices)))):
            if index != conNodeIndex:
                preferenceAdjMatrixValues[index][conNodeIndex] = rank + 1
                preferenceAdjMatrix[index][conNodeIndex] = 1
            else: 
                preferenceAdjMatrixValues[index][conNodeIndex] = 0
                preferenceAdjMatrix[index][conNodeIndex] = 0
    
    # print(preferenceAdjMatrixValues)
    adjMatrix = assignConnections(nodesColor, adjMatrix, nodesScore) #initially randomly assign all pairings

    testedEdges = []
    for rankCutoff in range(nNodes): #look at network created by edges representing ranking of node to connected node (directed graph). Start only looking at ranks >= 1, then >= 2, etc...
        rankCutoff += 1 
        preferenceAdjMatrixValuesCuttoff = np.copy(preferenceAdjMatrixValues) 
        preferenceAdjMatrixCuttoff = np.copy(preferenceAdjMatrix)
        for row, rowIndex in zip(preferenceAdjMatrixValuesCuttoff, list(range(np.shape(preferenceAdjMatrixValuesCuttoff)[0]))): #create new "preference adjacency matrix" with only ranks over threshold
            for value, valueIndex in zip(row, list(range(np.shape(preferenceAdjMatrixValuesCuttoff)[1]))):
                if value > rankCutoff:
                    preferenceAdjMatrixCuttoff[rowIndex][valueIndex] = 0 
                    preferenceAdjMatrixValuesCuttoff[rowIndex][valueIndex] = 0

        walksLen2 = np.linalg.matrix_power(preferenceAdjMatrixCuttoff, 2) #find anywhere were there is a path of length two from and back to node, meaning that both nodes have a preference for eachother above current theshold
        for pair, index in zip(np.diag(walksLen2), list(range(len(np.diag(walksLen2))))):
            if pair > 0: #find the above nodes where it has a possible pair
                testAdjMatrix = np.copy(adjMatrix) #create copy of current adjacency matrix to test if it is "better" with change of pairing
                for tempEdge, tempConIndex in zip(preferenceAdjMatrixCuttoff[index], list(range((len(preferenceAdjMatrixCuttoff[index]))))): #here we find the two nodes that have a possible pairing above and pair them together in the "test graph," then remove their previous connections and then find the nodes they were each connected to and connect them
                    if (index, tempConIndex) not in testedEdges and (tempConIndex, index) not in testedEdges:
                        if tempEdge == 1 and preferenceAdjMatrixCuttoff[tempConIndex][index] == 1:
                            tempConIndex1 = None
                            index1 = None
                            for edge, oldEdgeIndex in zip(testAdjMatrix[index], list(range(len(testAdjMatrix[index])))):
                                if edge == 1:
                                    tempConIndex1 = oldEdgeIndex
                                    testAdjMatrix[index][oldEdgeIndex] = 0 
                            for edge, oldEdgeIndex in zip(testAdjMatrix[tempConIndex], list(range(len(testAdjMatrix[tempConIndex])))):
                                if edge == 1:
                                    index1 = oldEdgeIndex
                                    testAdjMatrix[tempConIndex][oldEdgeIndex] = 0 

                            testAdjMatrix[index][tempConIndex] = 1 
                            testAdjMatrix[tempConIndex][index] = 1
                            testAdjMatrix[index1][tempConIndex1] = 1
                            testAdjMatrix[tempConIndex1][index1] = 1
                            if average_rank_sum(testAdjMatrix, preferenceAdjMatrixValues) < average_rank_sum(adjMatrix, preferenceAdjMatrixValues): #if this change resulted in a benefit for the average "betterment" for each pairing, this becomes to new adjacency matrix, otherwise forget about it
                                # print(str(average_rank_sum(adjMatrix, preferenceAdjMatrixValues)) + " > " + str(average_rank_sum(testAdjMatrix, preferenceAdjMatrixValues)))
                                adjMatrix = np.copy(testAdjMatrix)
                                
                            else: 
                                testAdjMatrix = np.copy(adjMatrix)
                            testedEdges.append((index, tempConIndex)) #record this tested edge to not be tested again, improving effeciency 
    return(adjMatrix)

