import math
import numpy as np
import matplotlib.pyplot as plt

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    expanded_nodes = []  # List to store all nodes that were in the open list

    # Add the start node
    open_list.append(start_node)
    expanded_nodes.append(start_node.position)  # Start node is added to expanded nodes

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            h = []
            current = current_node
            while current is not None:
                path.append(current.position)
                h.append(current.h)
                current = current.parent
            return path[::-1], expanded_nodes, h[::-1]  # Return reversed path and all expanded nodes

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Child is already in the closed list
            if new_node in closed_list:
                continue

            # Create the f, g, and h values
            new_node.g = current_node.g + 1
            #new_node.h = ((new_node.position[0] - end_node.position[0]) ** 2) + ((new_node.position[1] - end_node.position[1]) ** 2)
            dx = abs(new_node.position[0] - end_node.position[0])
            dy = abs(new_node.position[1] - end_node.position[1])
            new_node.h = dx + dy  # Manhattan
            #new_node.h = math.sqrt(dx**2 + dy**2)
            new_node.f = new_node.g + new_node.h

            # Child is already in the open list with a lower cost
            if any(open_node for open_node in open_list if new_node == open_node and new_node.g > open_node.g):
                continue

            # Add the child to the open list
            open_list.append(new_node)
            expanded_nodes.append(new_node.position)  # Add to expanded nodes

    return None, expanded_nodes   # If no path is found, return the expanded nodes


def visualize_maze(maze, path, expanded_nodes):
    # Crear una copia de la matriz del laberinto
    visual_maze = np.zeros((len(maze), len(maze[0]), 3), dtype=np.float32)

    # Asignar colores a cada celda
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:  # Pared -> Negro
                visual_maze[i, j] = [0, 0, 0]
            else:  # Espacio -> Blanco
                visual_maze[i, j] = [1, 1, 1]

    # Colorear los nodos expandidos -> Rojo
    for node in expanded_nodes:
        visual_maze[node[0], node[1]] = [1, 0, 0]

    # Colorear el camino solución -> Verde
    for position in path:
        visual_maze[position[0], position[1]] = [0, 1, 0]

    # Mostrar el laberinto
    plt.imshow(visual_maze, interpolation='nearest')
    plt.title("Laberinto con Camino y Nodos Expandidos")
    plt.axis('off')  # Ocultar los ejes
    plt.show()

def save_maze_figure(maze, path, expanded_nodes, filename="maze_solution.png"):
    # Crear una copia de la matriz del laberinto
    visual_maze = np.zeros((len(maze), len(maze[0]), 3), dtype=np.float32)

    # Asignar colores a cada celda
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:  # Pared -> Negro
                visual_maze[i, j] = [0, 0, 0]
            else:  # Espacio -> Blanco
                visual_maze[i, j] = [1, 1, 1]

    # Colorear los nodos expandidos -> Rojo
    for node in expanded_nodes:
        visual_maze[node[0], node[1]] = [1, 0, 0]

    # Colorear el camino solución -> Verde
    for position in path:
        visual_maze[position[0], position[1]] = [0, 1, 0]

    # Configurar la visualización
    plt.imshow(visual_maze, interpolation='nearest')
    plt.title("Laberinto con Camino y Nodos Expandidos")
    plt.axis('off')  # Ocultar los ejes

    # Guardar la figura
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()  # Cerrar la figura para liberar memoria
    print(f"Figura guardada como: {filename}")


def main():
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (2, 1)
    end = (12, 14)

    path, expanded_nodes, h = astar(maze, start, end)
    print("Path:", path)
    print("Expanded Nodes:", expanded_nodes)
    print("Heuristics:", h)

    # Visualizar el laberinto con la solución y nodos expandidos
    visualize_maze(maze, path, expanded_nodes)

    # Guardar la figura como archivo
    #save_maze_figure(maze, path, expanded_nodes, "maze_solution.png")


if __name__ == '__main__':
    main()

