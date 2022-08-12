import numpy as np
import copy
import time, math
import os, sys
class tiles:
    parent = None
    parentAction = None
    visited = False
    cost = 0
    depth = 0
    def __init__(self, state):
        self.state = state
    def __ref__(self):
        print(f"parent: {parent}\nstate: {state}\n")
    def setParent(parent, action):
        self.parent = parent
        self.action = action
    def getIndexElement(self, state, element):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if (state[i][j] == element):
                    return [i, j]   
    def getManhattanDistance(self, goal_state, tile):
        distance = 0
        for i in range(len(tile.state)):
            for j in range(len(tile.state[0])):
                if (goal_state[i][j] != tile.state[i][j]):
                    index_of_ele = self.getIndexElement(tile.state, goal_state[i][j])
                    distance = math.sqrt((index_of_ele[0] - i) ** 2 + (index_of_ele[1] - j) ** 2)
        return distance
    def getNumberOfMisplacedTiles(self, goal_state, tile):
        difference = np.array(goal_state) - np.array(tile.state)
        number_of_misplaced_tiles = np.count_nonzero(difference)
        return number_of_misplaced_tiles
    def getChildren(self, state, state_visited, goal_state, option):
        zeroIndex = self.getIndexElement(state, 0)
        childrenStates = self.getPossibleActions(state, zeroIndex[0], zeroIndex[1])
        children = []
        for ele in childrenStates:
            for a in ele:
                if (ele[a] not in state_visited):
                    childTile = tiles(ele[a])
                    childTile.parentAction = a
                    childTile.parent = self
                    childTile.visited = False
                    childTile.fx = self.depth + 1
                    if (option == 1):
                        cost = self.getNumberOfMisplacedTiles(goal_state, childTile)
                    else:
                        cost = self.getManhattanDistance(goal_state, childTile)
                    childTile.cost = childTile.fx + cost 
                    children.append(childTile)
        return children
    def getPossibleActions(self, oldState, r, c):
        state = copy.deepcopy(oldState)
        actions = []
        if (r + 1 < len(state)):
            copyState = copy.deepcopy(oldState)
            temp = copyState[r][c]
            copyState[r][c] = copyState[r + 1][c]
            copyState[r+1][c] = temp
            actions.append({'D': copyState}) 
        if (r - 1 >= 0):
            copyState = copy.deepcopy(oldState)
            temp = copyState[r][c]
            copyState[r][c] = copyState[r - 1][c]
            copyState[r-1][c] = temp
            actions.append({'U': copyState})
        if (c + 1 < len(state[0])):
            copyState = copy.deepcopy(oldState)
            temp = copyState[r][c]
            copyState[r][c] = state[r][c + 1]
            copyState[r][c + 1] = temp
            actions.append({'R': copyState})
        if (c - 1 >= 0):
            copyState = copy.deepcopy(oldState)
            temp = copyState[r][c]
            copyState[r][c] = copyState[r][c - 1]
            copyState[r][c - 1] = temp
            actions.append({'L': copyState})
        return actions
def main(option): 
    output = []
    queue = []
    state_visited = []
    goal_state = [[1, 2 ,3, 4],[ 5, 6, 7, 8],[ 9, 10, 11, 12],[13, 14, 15, 0]]
    def astar(queue, src, option):
        queue.append(src)
        while len(queue) != 0:
            s = queue.pop(0)
            s.visited = True
            state_visited.append(s.state)
            output.append(s)
            if (np.array_equal(s.state, goal_state)):
                return s
            children = s.getChildren(s.state, state_visited, goal_state, option)
            children.sort(key=lambda child: child.cost)
            for ele in children:
                if (ele.visited == False):
                    queue.append(ele)
    a = list(map(int, sys.argv[1: len(sys.argv)]))
    b = np.reshape(a, (4, 4))
    b = b.tolist()
    start = time.time()
    tile1 = tiles(b)
    tile1.depth = 0 
    goal_node = astar(queue, tile1, option)
    end = time.time()
    actions = []
    node = goal_node
    while (node.parent):
        actions.append(node.parentAction)
        node = node.parent
    print(actions[::-1])
    print(f"Number of nodes expanded: {len(output)}")
    print(f"Time taken: {end - start}")
    print(f"Memory usage: {(sys.getsizeof(output) + sys.getsizeof(state_visited)) / 1024} kb")
print(f"Output calculated with heuristic function as Misplaced tiles")
main(1)
print(f"Output calculated with heuristic function as Manhattan distance")
main(2)
