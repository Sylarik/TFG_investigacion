import numpy as np
import matplotlib.pyplot as plt
import time
import math

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None, velocidad=None):
        self.parent = parent        # Nodo padre que permite reconstruir la ruta al final.
        self.position = position    # posicion del nodo en la cuadricula
        self.direction = direction  # Dirección del movimiento en la cuadrícula (N, S, E, W, etc.).
        self.velocidad = velocidad  # Velocidad del barco en el nodo, se va a ir actualizando con la velocidad efectiva veff

        self.g = 0  #Costo desde el inicio hasta el nodo actual.
        self.h = 0  #Estimación heurística de la distancia al objetivo.
        self.f = 0  #Función de costo total.

    # verificamos si un nodo ya ha sido explorado
    def __eq__(self, other):
        return self.position == other.position #Se compara si dos nodos tienen la misma posición en el laberinto.

def astar_with_generated_nodes(maze, matriz_tuplas, start, end, start_direction, initial_speed):
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
    start_node = Node(None, start, start_direction, initial_speed)     #nodo de inicio en una posicion con una direccion
    start_node.g = start_node.h = start_node.f = 0      #Inicialización de costos en start_node
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = [start_node]    # Contiene nodos en espera de evaluación
    closed_list = []            # Contiene nodos ya evaluados.
    expanded_nodes = []         # Nodos expandidos
    generated_nodes = []        # Nodos generados pero no necesariamente expandidos

    # Loop until you find the end
    while len(open_list) > 0:                                       # Mientras 'open_list' tenga valores

        # 1. Cogemos el nodo que menor coste tenga de los nodos a evaluar y se convierte en el 'nodo actual'
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):                    # genera pares (índice, nodo) mientras se itera sobre open_list -> index almacena la posición en la lista, item almacena el nodo en esa posición
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # 2. Mover el nodo actual de open_list a closed_list
        open_list.pop(current_index)
        closed_list.append(current_node)
        expanded_nodes.append(current_node.position)  # Mark as expanded

        # 3. Encontrar el final
        if current_node.position == end_node.position:          # si el nodo actual es el final
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
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

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
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

            ## Create the f, g, and h values

            v_viento = ''   # segundo compenente de la tupla 
            vx_viento = ''  # v_viento * cos(ang_viento)
            vy_viento =''   # v_viento * sin(ang_viento)
            ang_viento = '' # primer componente de la tupla

            v_barco = ''    # velocidad del nodo antiguo
            vx_barco =''    # v_barco * cos(ang_barco)
            vy_barco =''    # v_barco * sin(ang_barco)
            ang_barco = 0   # siempre 0 ya que lo considero como punto de referencia

            #veff = v_total * math.cos(angulo_total)
            #current_node.g = 1 / veff

            new_node.g = current_node.g + 1                             #Costo desde el inicio hasta este nodo (+1 respecto al padre).
            new_node.h = (
                (new_node.position[0] - end_node.position[0]) ** 2 +    #Heurística: distancia euclidiana cuadrada al objetivo.
                (new_node.position[1] - end_node.position[1]) ** 2
            )
            new_node.f = new_node.g + new_node.h

            # Child is already in the open list with a lower cost
            if any(
                open_node for open_node in open_list
                if new_node == open_node and new_node.g > open_node.g
            ):
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

    fig, ax = plt.subplots()

    # Mostrar la imagen
    ax.imshow(visual_maze, interpolation='nearest')
    # Configurar el título
    ax.set_title("Laberinto con Camino, Nodos Expandidos y Generados")
    # Configurar la cuadrícula para que no sobresalga
    ax.set_xticks(np.arange(visual_maze.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(visual_maze.shape[0] + 1) - 0.5, minor=True)
    ax.grid(visible=True, color='black', linewidth=1, which='minor')
    # Ocultar los ticks de los ejes
    ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.show()

def verify_expanded_vs_solution(path, expanded_nodes):
    # Verificar si los nodos expandidos coinciden con el camino solución
    if set(path) == set(expanded_nodes):
        print("Todos los nodos expandidos coinciden con el camino solución.")
    else:
        print("Hay nodos expandidos que no forman parte del camino solución.")

def main():
    started = time.perf_counter()
    
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    matriz_tuplas = [
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)],
        [(-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3), (-90, 3)]
    ]      
    
    #maze = np.loadtxt("land_mask.txt", dtype=int)

    start = (1,1)
    end = (8,8)
    start_direction = 'S'
    velocidad = 10
    path, expanded_nodes, generated_nodes = astar_with_generated_nodes(maze, matriz_tuplas, start, end, start_direction, velocidad)

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
    
