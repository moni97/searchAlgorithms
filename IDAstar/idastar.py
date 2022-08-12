import random
import math
import time
import psutil
import os
from collections import deque
import sys
import numpy as np
#This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self,tiles):
        self.size = int(math.sqrt(len(tiles))) # defining length/width of the board
        self.tiles = tiles

    #This function returns the resulting state from taking particular action from current state
    def execute_action(self,action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action=='L':	
            if empty_index%self.size>0:
                new_tiles[empty_index-1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-1]
        if action=='R':
            if empty_index%self.size<(self.size-1): 	
                new_tiles[empty_index+1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+1]
        if action=='U':
            if empty_index-self.size>=0:
                new_tiles[empty_index-self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-self.size]
        if action=='D':
            if empty_index+self.size < self.size*self.size:
                new_tiles[empty_index+self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+self.size]
        return Board(new_tiles)


#This class defines the node on the search tree, consisting of state, parent and previous action		
class Node:
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = 0
    #Returns string representation of the state	
    def __repr__(self):
        return str(self.state.tiles)

    #Comparing current node with other node. They are equal if states are equal	
    def __eq__(self,other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))

#Utility function to randomly generate 15-puzzle		
def generate_puzzle(size):
    numbers = list(range(size*size))
    random.shuffle(numbers)
    return Node(Board(numbers),None,None)

def getNumberOfMisplacedTiles(goal_state, node):
    n = node.state.tiles
    number_of_misplaced_tiles = 0
    for i in range(len(goal_state)):
        if not n[i] == goal_state[i]:
             number_of_misplaced_tiles += 1
    return number_of_misplaced_tiles

def getManhattanDistance(child_state):
    goal_state = get_goal()
    size_of_child_state = child_state.state.size
    goal_state_array = np.array(goal_state)
    goal_state_array = np.reshape(goal_state_array, (size_of_child_state, size_of_child_state))
    target_array = np.array(child_state.state.tiles)
    target_array = np.reshape(target_array, (size_of_child_state, size_of_child_state))
    manhattan_distance = 0
    for j in child_state.state.tiles:
        x_val,y_val = np.where(target_array == j)
        x_goal,y_goal = np.where(goal_state_array == j)
        manhattan_distance = abs(x_val - x_goal) + abs(y_val - y_goal) + manhattan_distance
    return manhattan_distance

#This function returns the list of children obtained after simulating the actions on current node
def get_children(parent_node, heuristic_function):
    children = []
    actions = ['L','R','U','D'] # left,right, up , down ; actions define direction of movement of empty tile
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        child_node = Node(child_state,parent_node,action)
        if (heuristic_function == 1):
            child_node.cost = getNumberOfMisplacedTiles(get_goal(), child_node)
        else:
            child_node.cost = getManhattanDistance(child_node)
        children.append(child_node)
    return children

#This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
def find_path(node):	
    path = []	
    while(node.parent is not None):
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path

def ida_star(root_node, heuristic_function):
    start_time = time.time()
    bound = root_node.cost
    path = deque([root_node])
    explored = set()
    iteration = 0
    while(True):
        print(f"iteration {iteration}")
        explored.clear()
        found, final_path, no_of_nodes, cost = search(path, 0, bound, explored, heuristic_function)
        if found == 'FOUND':
            end_time = time.time()
            return final_path, no_of_nodes, (end_time - start_time), sys.getsizeof(explored)
        if cost == float('inf'):
            return 'NOT FOUND'
        bound = cost
        iteration += 1

def search(path, g, bound, explored, heuristic_function):
    node = path[-1]
    f = g + node.cost
    if f > bound:
        return 'NOT FOUND', None, None, f
    if goal_test(node):
        return 'FOUND', find_path(node), len(explored), None
    mininum_cost = float('inf')
    children = get_children(node, heuristic_function)
    for succ in children:
        if succ not in path:
            path.append(succ)
            explored.add(succ)
            found, final_path, no_of_nodes, cost = search(path, g + 1, bound, explored, heuristic_function)
            if (found == 'FOUND'):
                return 'FOUND', final_path, len(explored), None 
            if (cost < mininum_cost):
                mininum_cost = cost
            path.pop()
    return 'NOT FOUND', None, None, mininum_cost

#Main function accepting input from console , runnung bfs and showing output	
def main():
    initial = str(input("initial configuration: "))
    heuristic_function = input("Type the required input to choose the heuristic function\n1. Number of misplaced tiles\n2. Manhattan distance\n")
    heuristic_function = int(heuristic_function)
    initial_list = initial.split(" ")
    root = Node(Board(initial_list),None,None)
    if (heuristic_function == 1):
        root.cost = getNumberOfMisplacedTiles(get_goal(), root)
    else:
        root.cost = getManhattanDistance(root)
    path, expanded_nodes, time_taken, memory_consumed = ida_star(root, heuristic_function)
    print("Moves: " + " ".join(path))
    print("Number of expanded Nodes: "+ str(expanded_nodes))
    print("Time Taken: " + str(time_taken))
    print("Max Memory (Bytes): " +  str(memory_consumed))

#Utility function checking if current state is goal state or not
def goal_test(cur_tiles):
    return cur_tiles.state.tiles == ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']

def get_goal():
    return ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']
# 5 2 4 8 10 3 11 14 6 0 9 12 13 1 15 7
if __name__=="__main__":main()
