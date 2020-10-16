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

def rank_choices(nodeColor, nodeIndex, nodesScore, prevNodesScore):
    scoredNodes = []
    nNodes = len(nodesScore)
    if nodeColor == 'red':
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            nRounds = len(prevNodesScore[index]) + 1
            avgScore = currentScore/nRounds #could also look at average over last 5 rounds or something 
            
            assignedScore = random.random() #random selection
            scoredNodes.append((index, assignedScore))

    elif nodeColor == 'green':
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            nRounds = len(prevNodesScore[index]) + 1
            avgScore = currentScore/nRounds #could also look at average over last 5 rounds or something 
            
            assignedScore = random.random() #random selection
            scoredNodes.append((index, assignedScore))

    elif nodeColor == "blue":
        for index in list(range(nNodes)):
            currentScore = nodesScore[index]
            nRounds = len(prevNodesScore[index]) + 1
            avgScore = currentScore/nRounds #could also look at average over last 5 rounds or something 
            
            assignedScore = random.random() #random selection
            scoredNodes.append((index, assignedScore))

    scoredNodesRanked = sorted(scoredNodes, reverse=True, key=lambda score: score[1]) #citation: https://docs.python.org/3/howto/sorting.html
    rankedChoices = [score[1] for score in scoredNodesRanked]
    return(rankedChoices)