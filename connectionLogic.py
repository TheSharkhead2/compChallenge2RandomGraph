import random 

def check_can_connect(endingNodeIndex, adjMatrix):
    for edge in adjMatrix[endingNodeIndex]:
        if edge == 1:
            # print("{} is bad".format(endingNodeIndex))
            return(False)
    # print("{} is GOOD".format(endingNodeIndex))
    return(True)

def choose_connection(nodeIndex, nodeColor, nodesScore, prevNodesScore, adjMatrix, prevAdjMatrix): #explore allowing all players to rank choices and then maxamise the utility of each player 
    if not check_can_connect(nodeIndex, adjMatrix):
        return(adjMatrix)
    nodesNetGain = [newscore-oldscore for (oldscore, newscore) in zip(prevNodesScore, nodesScore)]
    nNodes = len(nodesScore)
    possibleConnections = [n for n in list(range(nNodes)) if check_can_connect(n, adjMatrix) and n != nodeIndex]
    
    preferedConnection = random.choice(possibleConnections)
    adjMatrix[nodeIndex][preferedConnection] = 1 
    adjMatrix[preferedConnection][nodeIndex] = 1
    return(adjMatrix)

