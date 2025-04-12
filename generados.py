import time
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


def astar_with_generated_nodes(maze, start, end):
    """Returns path, expanded_nodes, and generated_nodes for A* Pathfinding"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    expanded_nodes = []  # List of expanded nodes
    generated_nodes = []  # List of generated nodes

    # Add the start node
    open_list.append(start_node)

    

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
        expanded_nodes.append(current_node.position)  # Mark as expanded

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], expanded_nodes, generated_nodes

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                #print("node:",node_position)

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
            new_node.h = ((new_node.position[0] - end_node.position[0]) ** 2) + ((new_node.position[1] - end_node.position[1]) ** 2)
            new_node.f = new_node.g + new_node.h

            # Child is already in the open list with a lower cost
            if any(open_node for open_node in open_list if new_node == open_node and new_node.g > open_node.g):
                continue

            # Add the child to the open list
            open_list.append(new_node)

            # Add to generated nodes if not already added
            if new_node.position not in generated_nodes:
                generated_nodes.append(new_node.position)

    return None, expanded_nodes, generated_nodes


def visualize_maze_with_generated(maze, path, expanded_nodes, generated_nodes):
    # Crear una copia de la matriz del laberinto
    visual_maze = np.zeros((len(maze), len(maze[0]), 3), dtype=np.float32)

    # Asignar colores a cada celda
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:  # Pared -> Negro
                visual_maze[i, j] = [0, 0, 0]
            else:  # Espacio -> Blanco
                visual_maze[i, j] = [1, 1, 1]

    # Colorear los nodos generados -> Azul
    for node in generated_nodes:
        visual_maze[node[0], node[1]] = [0, 0, 1]

    # Colorear los nodos expandidos -> Rojo
    for node in expanded_nodes:
        visual_maze[node[0], node[1]] = [1, 0, 0]

    # Colorear el camino solución -> Verde
    for position in path:
        visual_maze[position[0], position[1]] = [0, 1, 0]

    # Mostrar el laberinto
    plt.imshow(visual_maze, interpolation='nearest')
    plt.title("Laberinto con Camino, Nodos Expandidos y Generados")
    plt.axis('off')  # Ocultar los ejes
    plt.show()

def verify_expanded_vs_solution(path, expanded_nodes):
    # Verificar si los nodos expandidos coinciden con el camino solución
    if set(path) == set(expanded_nodes):
        print("Todos los nodos expandidos coinciden con el camino solución.")
    else:
        print("Hay nodos expandidos que no forman parte del camino solución.")


def main():
    started = time.perf_counter()
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

    path, expanded_nodes, generated_nodes = astar_with_generated_nodes(maze, start, end)
    print("Path:", path)
    print("Expanded Nodes:", expanded_nodes)
    print(f"Total Expanded Nodes: {len(expanded_nodes)}")

    print("Generated Nodes:", generated_nodes)
    print(f"Total Generated Nodes: {len(generated_nodes)}")


    # Verificar si los nodos expandidos coinciden con el camino solución
    verify_expanded_vs_solution(path, expanded_nodes)

    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - started:.6f} segundos")

    # Visualizar el laberinto con la solución, nodos expandidos y generados
    visualize_maze_with_generated(maze, path, expanded_nodes, generated_nodes)


if __name__ == '__main__':
    main()
