import math
import numpy as np
import matplotlib.pyplot as plt
import time

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None):
        self.parent = parent        # Nodo padre que permite reconstruir la ruta al final.
        self.position = position    # posicion del nodo en la cuadricula
        self.direction = direction  # Dirección del movimiento en la cuadrícula (N, S, E, W, etc.).

        self.g = 0  #Costo desde el inicio hasta el nodo actual.
        self.h = 0  #Estimación heurística de la distancia al objetivo.
        self.f = 0  #Función de costo total.

    # verificamos si un nodo ya ha sido explorado
    def __eq__(self, other):
        return self.position == other.position #Se compara si dos nodos tienen la misma posición en el laberinto.

def a_star_pathfinding(maze, start, end, start_direction):
    """Returns path, expanded_nodes, and generated_nodes for A* Pathfinding"""

    # Define allowed directions as a list of tuples
    direction_vectors = [
        ('N', [(-1, 0), (-1, -1), (-1, 1)]),  # North
        ('S', [(1, 0), (1, -1), (1, 1)]),    # South
        ('E', [(0, 1), (-1, 1), (1, 1)]),    # East
        ('W', [(0, -1), (-1, -1), (1, -1)]), # West
        ('NW', [(-1, -1), (-1, 0), (0, -1)]), # North-West
        ('NE', [(-1, 1), (-1, 0), (0, 1)]),  # North-East
        ('SW', [(1, -1), (1, 0), (0, -1)]),  # South-West
        ('SE', [(1, 1), (1, 0), (0, 1)])     # South-East
    ]

    directions = [
        ('N', [(-1, 0)]),
        ('S', [(1, 0)]),
        ('E', [(0, 1)]),
        ('W', [(0, -1)]),
        ('NW', [(-1, -1)]),
        ('NE', [(-1, 1)]),
        ('SW', [(1, -1)]),
        ('SE', [(1, 1)])
    ]

    # Create start and end nodes
    start_node = Node(None, start, start_direction)     #nodo de inicio en una posicion con una direccion 
    end_node = Node(None, end)

    # Initialize both open and closed list
    open_list = [start_node]    # Contiene nodos en espera de evaluación
    closed_list = []            # Contiene nodos ya evaluados.
    expanded_nodes = []         # Nodos expandidos
    generated_nodes = []        # Nodos generados pero no necesariamente expandidos

    # Loop until you find the end
    while open_list:                                       # Mientras 'open_list' tenga valores

        # 1. Cogemos el nodo que menor coste tenga de los nodos a evaluar y se convierte en el 'nodo actual'
        current_node = open_list[0]
        for node in open_list:
            if node.f < current_node.f:
                current_node = node

        # 2. Mover el nodo actual de open_list a closed_list
        open_list.remove(current_node)
        closed_list.append(current_node)
        expanded_nodes.append(current_node.position)  # Mark as expanded

        # 3. Encontrar el final
        if current_node == end_node:          # si el nodo actual es el final
            path = []
            temp = current_node
            while temp:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1], expanded_nodes, generated_nodes  # Se retorna el camino invertido ([::-1]), ya que fue construido desde el final al inicio.

        # 4. Generar nodos hijos
        #valid_moves = next(moves for direction, moves in direction_vectors if direction == current_node.direction)  # Solo selecciona la tupla donde direction coincida con current_node.direction
        
        # Segun la direccion a la que apunte el barco, va a tener una serie de movimientos u otros, en total 3 tipos
        valid_moves = []
        for direction, moves in direction_vectors:
            if direction == current_node.direction:
                valid_moves = moves

        #Por cada casilla a la que se puede mover
        for new_position in valid_moves:

            # Get node position -> tiene la posicion del nuevo nodo (131,440)
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1]
            )

            # Validar límites
            if not (0 <= node_position[0] < len(maze)) or not (0 <= node_position[1] < len(maze[0])):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Determine the new direction based on the move
            #new_direction = next(
            #    direction for direction, moves in direction_vectors if new_position in moves
            #)
            '''
            new_direction = next(
                direction for direction, moves in directions if new_position in moves
            )
            '''
            new_direction = ''
            for direction, moves in directions:
                if new_position in moves:
                    new_direction = direction

            # Create new node
            new_node = Node(current_node, node_position, new_direction)     # padre, posicion, direccion

            # Child is already in the closed list
            if new_node in closed_list:             #con 'in' lo que se hace es llamar internamente a __equal__, poruqe es una CLASE
                continue                            #el operador 'in' recorre la lista closed_list y compara cada elemento con new_node

            # Create the f, g, and h values
            new_node.g = current_node.g + 1
            dx = abs(new_node.position[0] - end_node.position[0])
            dy = abs(new_node.position[1] - end_node.position[1])
            new_node.h = math.sqrt(dx**2 + dy**2)  # Euclidiana
            new_node.f = new_node.g + new_node.h

            for existing_node in open_list:
                if new_node == existing_node:
                    if new_node.g < existing_node.g:
                        open_list.remove(existing_node)
                        open_list.append(new_node)
                    break
            else:
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
    
    #maze = np.loadtxt("land_mask.txt", dtype=int)
    '''
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
'''
    start = (2, 1)#(130, 440) #(19,1)
    end = (12, 14) #(426, 862)#(1,19)
    start_direction = 'NW' #'S'

    path, expanded_nodes, generated_nodes = a_star_pathfinding(maze, start, end, start_direction)

    if path is None:
        print("No se encontró un camino válido desde el inicio hasta el objetivo.")
        return

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
    
