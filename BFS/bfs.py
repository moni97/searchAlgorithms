import numpy as np
import copy
import time
import sys
# Class that contains the tile information and the actions that are possible with the tiles
# parent - represents the parent tile positions
# parentAction - the action by which the current tile positions are applied
class tiles:
    parent = None
    parentAction = None
    visited = False
    def __init__(self, state):
        self.state = state
    def __ref__(self):
        print(f"parent: {parent}\nstate: {state}\n")
    def setParent(parent, action):
        self.parent = parent
        self.action = action
    def getIndexZero(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if (state[i][j] == 0):
                    return [i, j]    
    def getChildren(self, state, state_visited):
        zeroIndex = self.getIndexZero(state)
        childrenStates = self.getPossibleActions(state, zeroIndex[0], zeroIndex[1])
        children = []
        for ele in childrenStates:
            for a in ele:
                if (ele[a] not in state_visited):
                    childTile = tiles(ele[a])
                    childTile.parentAction = a
                    childTile.parent = self
                    childTile.visited = False
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
output = []
queue = []
state_visited = []
goal_state = [[1, 2 ,3, 4],[ 5, 6, 7, 8],[ 9, 10, 11, 12],[13, 14, 15, 0]]

def bfs(queue, src):
    queue.append(src)
    while len(queue) != 0:
        s = queue.pop(0)
        s.visited = True
        state_visited.append(s.state)
        output.append(s)
        if (np.array_equal(s.state, goal_state)):
            return s
        children = s.getChildren(s.state, state_visited)
        for ele in children:
            if (ele.visited == False):
                queue.append(ele)
print(sys.argv[1:])

# Convert the input from CLA to matrices
a = list(map(int, sys.argv[1: len(sys.argv)]))
b = np.reshape(a, (4, 4))
b = b.tolist()
# Start the time to get the time taken to search
start = time.time()
tile1 = tiles(b)
goal_node = bfs(queue, tile1)
end = time.time()
# End the time started

actions = []
node = goal_node
# Get the actions to get the path to the goal state
while (node.parent):
    actions.append(node.parentAction)
    node = node.parent

# Print the results
print(actions[::-1])
print(f"Number of nodes expanded: {len(output)}")
print(f"Time taken: {end - start}")
print(f"Memory usage: {(sys.getsizeof(output) + sys.getsizeof(state_visited)) / 1024} kb")
