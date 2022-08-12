import numpy as np
import copy
import time, math
import os, sys
from queue import LifoQueue

# Variable to check for memory usage
memory_usage = 0

# Class that stores the details of every tile
class tiles:
    parent = None
    parentAction = None
    visited = False
    depth = None
    def __init__(self, state):
        self.state = state
    # Function to return the index of the empty tile
    def getIndexZero(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if (state[i][j] == 0):
                    return [i, j]
    # Returns the children of a node
    def getChildren(self, state):
        global memory_usage
        zeroIndex = self.getIndexZero(state)
        childrenStates = self.getPossibleStates(state, zeroIndex[0], zeroIndex[1])
        children = []
        for ele in childrenStates:
            for a in ele:
                childTile = tiles(ele[a])
                childTile.parentAction = a
                childTile.parent = self
                childTile.visited = False
                childTile.depth = self.depth + 1
                children.append(childTile)
        return children
    # Returns the next possible actions on a tile
    def getPossibleStates(self, oldState, r, c):
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

# Initialize the arrays
lifo_queue = LifoQueue()
goal_state = [[1, 2 ,3, 4],[ 5, 6, 7, 8],[ 9, 10, 11, 12],[13, 14, 15, 0]]
cutoff = 1
failure = 0

# Get the input from command line arguments
a = list(map(int, sys.argv[1: len(sys.argv)]))
a = list(map(int, a))

# Convert the input string to a 4x4 matrix
b = np.reshape(a, (4, 4))
b = b.tolist()

# To measure the runtime of the algorithm
start = time.time()

# Initial state
tile1 = tiles(b)
tile1.depth = 0
memory_usage += sys.getsizeof(tile1)

def iterative_deepening(lifo_queue, src, numberOfNodes):
    global memory_usage
    limit = 0
    cutoff = 1
    limited_dfs_result = cutoff
    while (limited_dfs_result):
        state_visited = []
        limited_dfs_result = limited_dfs(lifo_queue, src, limit, state_visited, numberOfNodes)
        memory_usage += sys.getsizeof(state_visited) + sys.getsizeof(lifo_queue)
        numberOfNodes += len(state_visited)
        if (limited_dfs_result != cutoff):
            return limited_dfs_result
        limit += 1

def limited_dfs(lifo_queue, src, l, state_visited, numberOfNodes):
    global memory_usage
    lifo_queue.put(src)
    result = 0
    while (lifo_queue.empty() == False):
        current_node = lifo_queue.get()
        current_node.visited = True
        state_visited.append(current_node.state)
        if (np.array_equal(current_node.state, goal_state)):
            # curren_node => the node that contains the goal state
            # state_visited => number of nodes expanded
            return [current_node, numberOfNodes]
        if (current_node.depth > l):
            result = 1
        else: 
            children = current_node.getChildren(current_node.state)
            for ele in children:
                memory_usage += sys.getsizeof(ele)
                # state_visited keeps track of all the state that has been visited
                # by checking if a child is present in state_visited we can avoid cycles
                if ele.state not in state_visited and ele.visited == False:
                    lifo_queue.put(ele)
    return result

numberOfNodes = 0

# Call IDDFS
dfs_output = iterative_deepening(lifo_queue, tile1, numberOfNodes)

# End timer 
end = time.time()

# Get the set of actions from the goal state
node = dfs_output[0]
if node == failure:
    print('Failed to find the goal')
else:
    actions = []
    while (node.parent):
        actions.append(node.parentAction)
        node = node.parent

    # Print the outputs
    print(actions[::-1])
    print(f"Number of nodes expanded: {dfs_output[1]}")
    print(f"Time taken: {end - start}")
    print(f"Memory usage: { memory_usage / 1024} kb")
