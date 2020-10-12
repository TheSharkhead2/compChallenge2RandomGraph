import random 
import numpy as np
import networkx as nx #used this for help: https://www.python-course.eu/networkx.php & for coloring nodes: https://stackoverflow.com/questions/27030473/how-to-set-colors-for-nodes-in-networkx
import matplotlib.pyplot as plt
from connectionLogic import choose_connection

payoffMatrix = np.array([[(3,3), (0,5)], [(5,0), (1,1)]])

def display_graph(nodesColor, adjMatrix):
    G = nx.Graph()
    G.add_nodes_from(list(range(len(nodesColor))))
    
    edges = []
    rowIndex = 0
    for row in adjMatrix:
        edgeIndex = 0
        for edge in row:
            if edge == 1 and (edgeIndex, rowIndex) not in edges: #look for edge between two nodes and make sure that "duplicate" of edge not already accounted for
                edges.append((rowIndex, edgeIndex))
            edgeIndex += 1
        rowIndex += 1
    G.add_edges_from(edges)
    nx.draw(G, node_color=nodesColor)
    plt.show()

def gen_node_list(numnodes, randomColor=False, pR=False, pB=False, pG=False):
    nodeList = []
    if not randomColor: 
        if numnodes % 3 != 0:
            raise Exception("{} is not divisable by 3 and is therefore unable to be evenly split between red, green, and blue".format(numnodes))
        else:
            quantityColor = int(numnodes*2/3)
            for x in range(quantityColor): #weird way of creating r/b/g node labels 
                nodeList.append('red')
                nodeList.append('blue')
                nodeList.append('green')

    else:
        if not pR or not pB or not pG or pR+pB+pG != 1:
            raise Exception("Probabilities given: [{},{},{}] either are not given or don't add to 1".format(pR, pB, pG))
        for x in range(numnodes*2):
            randValue = random.random()
            if randValue < pR:
                nodeList.append('red')
            elif randValue < pR + pB:
                nodeList.append('blue')
            elif randValue < pR + pB + pG: 
                nodeList.append('green')
    return(nodeList)

def assignConnections(nodeList, adjMatrix, nodesScore):
    adjMatrix = np.zeros([len(nodeList), len(nodeList)])
    originalAdjMatrix = adjMatrix
    index = 0
    for node in nodeList:
        adjMatrix = choose_connection(index, node, nodesScore, nodesScore, adjMatrix, originalAdjMatrix)
        index += 1
    return(adjMatrix)

def node_move(node, index, nodesOppLastMove):
    if node == "green":
        move = nodesOppLastMove[index]
    elif node == "red":
        move = 1
    elif node == "blue":
        move = 0
    return int(move)

def play_round(nodeList, adjMatrix, nodesScore, nodesOppLastMove):
    nodesGone = []
    index = 0
    for node in nodeList:
        if index not in nodesGone:
            nodesGone.append(index)
            move = node_move(node, index, nodesOppLastMove)

            oppIndexTemp = 0 
            for edge in adjMatrix[index]:
                if edge == 1:
                    oppIndex = oppIndexTemp
                    break
                oppIndexTemp += 1
            oppMove = node_move(nodeList[oppIndex], oppIndex, nodesOppLastMove)

            score = payoffMatrix[move][oppMove]
            nodesScore[index] += score[0]
            nodesScore[oppIndex] += score[1]
            nodesOppLastMove[index] = oppMove
            nodesOppLastMove[oppIndex] = move
            nodesGone.append(index)
            nodesGone.append(oppIndex)
        index += 1 

def analytics_averageScore(nodesColor, scoreHistory):
    totalNodeScoreCount = [(0,0), (0,0), (0,0)] #first index red, then green, then blue... tuple, first index count second score
    for color, index in zip(nodesColor, list(range(len(nodesColor)))):
        if color == 'red':
            totalNodeScoreCount[0] = (totalNodeScoreCount[0][0] + 1,scoreHistory[-1][index])
        elif color == 'green':
            totalNodeScoreCount[1] = (totalNodeScoreCount[1][0] + 1,scoreHistory[-1][index])
        elif color == 'blue':
            totalNodeScoreCount[2] = (totalNodeScoreCount[2][0] + 1,scoreHistory[-1][index])
    averageScores = (totalNodeScoreCount[0][1]/totalNodeScoreCount[0][0], totalNodeScoreCount[1][1]/totalNodeScoreCount[1][0], totalNodeScoreCount[2][1]/totalNodeScoreCount[2][0])
    print(totalNodeScoreCount)
    print("red nodes had an average score of: {}, green with: {}, blue with: {}".format(averageScores[0], averageScores[1], averageScores[2]))
    return(averageScores)

nNodes = 9 #half total nodes



displayGraph = False
nRounds = 100
nGames = 100

averageScoreHistory = []

for game in range(nGames):
    nodesColor = gen_node_list(nNodes)
    nodesScore = np.zeros(2*nNodes)
    adjMatrix = np.zeros([2*nNodes,2*nNodes])
    nodesOppLastMove = np.ones(2*nNodes)
    scoreHistory = []
    adjMatrix = assignConnections(nodesColor, adjMatrix, nodesScore)
    if displayGraph:
        display_graph(nodesColor, adjMatrix)
        print(nodesScore)
    for Round in range(nRounds):
        play_round(nodesColor, adjMatrix, nodesScore, nodesOppLastMove)
        scoreHistory.append(nodesScore)
        adjMatrix = assignConnections(nodesColor, adjMatrix, nodesScore)
        if displayGraph:
            display_graph(nodesColor, adjMatrix)
            print(nodesScore)

    # print(scoreHistory)
    averageScoreHistory.append(analytics_averageScore(nodesColor, scoreHistory))

redScore = 0
greenScore = 0 
blueScore = 0 

for scores in averageScoreHistory:
    redScore += scores[0]
    greenScore += scores[1]
    blueScore += scores[2]

redScore = redScore/nGames
greenScore = greenScore/nGames
blueScore = blueScore/nGames

print("over {} games with {} rounds, red had on average {} points per game, green had {} points, and blue had {} points".format(nGames, nRounds, redScore, greenScore, blueScore))