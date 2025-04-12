import numpy as np # type: ignore
import pandas as pd # type: ignore
from queue import Queue
import heapq
import networkx as nx # type: ignore
import plotly.graph_objects as go # type: ignore
import time
from memory_profiler import profile, memory_usage # type: ignore
from matplotlib import pyplot as plt # type: ignore
from PIL import Image # type: ignore
from scipy.spatial import distance # type: ignore



grid_original = np.asarray(pd.read_csv('./mapa.csv').iloc[:, 1:])

grid_original.shape


initial_position = np.asarray(pd.read_csv('./start.csv').iloc[:, 1:])[:, 0]
last_position = np.asarray(pd.read_csv('./target.csv').iloc[:, 1:])[:, 0]

initial_position = (initial_position[0], initial_position[1])
last_position = (last_position[0], last_position[1])

initial_position, last_position


initial_grid = grid_original.copy()
initial_grid[initial_position[0], initial_position[1]] = 'X'

objective_grid = grid_original.copy()
objective_grid[last_position[0], last_position[1]] = 'X'


operations = [
                [ 0, -1], #left
                [-1,  0], #up
                [ 1,  0], #down
                [ 0,  1] #right
             ]


class Node:
    def __init__(self, value, level, cost, parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        self.level = level
        self.cost = cost

    def add_child(self, child):
        node = Node(child, self.level + 1, distance.euclidean(child, last_position),  parent=self)
        self.children.append(node)
        return node
    
    def __lt__(self, other):
        return self.cost < other.cost

class Tree:
    def __init__(self, root):
        self.root = root
         
def find_path_to_root(objective_node):
    path = []
    current_node = objective_node
    while current_node is not None:
        path.insert(0, current_node.value)
        current_node = current_node.parent
    return path


def generate_children(grid, operations, position):
    def change_position(operation):
        if grid[position[0] + operation[0], position[1] + operation[1]] != '#':
            return (position[0] + operation[0], position[1] + operation[1])
        
        else:
            return None
    
    children = []
    grid[position[0], position[1]] = 'X'
    
    '''
        Left
    '''
    if position[1] != 0:
        new_position = change_position(operations[0])
        
        if new_position is not None:
            children.append(new_position)
    
    '''
        Up
    '''
    if position[0] != 0:
        new_position = change_position(operations[1])
        
        if new_position is not None:
            children.append(new_position)
        
    '''
        Down
    '''
    if position[0] != grid.shape[0] - 1:
        new_position = change_position(operations[2])
        
        if new_position is not None:
            children.append(new_position)
        
    '''
        Right
    '''
    if position[1] != grid.shape[1] - 1:
        new_position = change_position(operations[3])
        
        if new_position is not None:
            children.append(new_position)
        
    return children


def construct_solution_A_labyrinth(tree):
    nodes_to_expand = []
    visited_nodes = []
    
    heapq.heappush(nodes_to_expand, tree.root)

    found = False
    path = []

    while not found:
        current_node = heapq.heappop(nodes_to_expand)
        current_position = current_node.value

        visited_nodes.append(current_position)
        children = generate_children(grid, operations, current_position)
        
        for c in children:
            if c not in visited_nodes:
                child = current_node.add_child(c)
                heapq.heappush(nodes_to_expand, child)

                if np.array_equal(c, last_position):
                    found = True
                    path = find_path_to_root(child)
                    visited_nodes.append(last_position)
                    break
                    
    return tree, path, visited_nodes


grid = initial_grid.copy()


start_time = time.time()

root = Tree(Node(initial_position, 0, distance.euclidean(initial_position, last_position)))
tree, solution_path, visited_nodes = construct_solution_A_labyrinth(root)

time.time() - start_time


#solution_path
def movements_to_solution(solution_path):
    movements = []
    operations = { (0, -1):'left', (-1, 0): 'up', (1, 0): 'down', (0, 1): 'right' }
    
    for i in range(len(solution_path) - 1):
        position_1 = solution_path[i]
        position_2 = solution_path[i + 1]
    
        movements.append(operations[((position_2[0] - position_1[0]),(position_2[1] - position_1[1]))])
        
    return movements


movements = movements_to_solution(solution_path)


#movements
def solution_graphical_representation(grid, solution_path, visited_nodes):
    grids_to_solution = []
    grids_to_solution.append(grid.copy())

    current_grid = grid.copy()  # Initialize current_grid outside the loop
    
    for i, node in enumerate(visited_nodes):
        current_grid = grids_to_solution[i].copy()

        if node in solution_path:
            current_grid[node[0]][node[1]] = 'X'
        else:
            current_grid[node[0]][node[1]] = 'O'

        grids_to_solution.append(current_grid)

    return grids_to_solution
grid_representation = grid_original.copy()
grids = solution_graphical_representation(grid_representation, solution_path, visited_nodes)
def conversion(labyrinth):
    color_map = {'#': (0, 0, 0), ' ': (1, 1, 1), 'O': (1, 0, 0), 'X': (0, 1, 0)}

    color_labyrinth = np.empty((labyrinth.shape[0], labyrinth.shape[1], 3))
    
    for i in range(labyrinth.shape[0]):
        for j in range(labyrinth.shape[1]):
            color_labyrinth[i, j] = color_map[labyrinth[i, j]]

    return color_labyrinth
converted_grid = conversion(grids[-1])

converted_grid = np.asarray(converted_grid, dtype=np.int64)

converted_grid.shape


image = Image.fromarray((converted_grid*255).astype(np.uint8))
fig, ax = plt.subplots(figsize=(15,15)  )

plt.imshow(image)
plt.axis('off')
plt.show()