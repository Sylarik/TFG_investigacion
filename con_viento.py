import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import os

from holgura import agregar_holgura

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, direction=None, velocity: float=None):
        self.parent = parent        # Nodo padre que permite reconstruir la ruta al final.
        self.position = position    # posicion del nodo en la cuadricula
        self.direction = direction  # Dirección del movimiento en la cuadrícula (N, S, E, W, etc.).
        self.velocity = velocity    # Velocidad del barco en la dirección del movimiento. | Al principio cte

        self.g = 0  #Costo desde el inicio hasta el nodo actual.
        self.h = 0  #Estimación heurística de la distancia al objetivo.
        self.f = 0  #Función de costo total.

    # verificamos si un nodo ya ha sido explorado
    def __eq__(self, other):
        return self.position == other.position #Se compara si dos nodos tienen la misma posición en el laberinto.

def astar_with_generated_nodes(maze, velocidad_viento, direccion_viento, start, end, start_direction, start_velocity):
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
    start_node = Node(None, start, start_direction, start_velocity)     #nodo de inicio en una posicion con una direccion
    start_node.g = start_node.h = start_node.f = 0      #Inicialización de costos en start_node
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = [start_node]    # Contiene nodos en espera de evaluación
    closed_list = []            # Contiene nodos ya evaluados.
    expanded_nodes = []         # Nodos expandidos
    generated_nodes = []        # Nodos generados pero no necesariamente expandidos
    #---
    
    ooo = 0
    # Loop until you find the end
    while len(open_list) > 0:                                       # Mientras 'open_list' tenga valores
        
        # 1. Cogemos el nodo que menor coste tenga de los nodos a evaluar y se convierte en el 'nodo actual'
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):                    # genera pares (índice, nodo) mientras se itera sobre open_list -> index almacena la posición en la lista, item almacena el nodo en esa posición
            print("FFFFFFFFFFFFF: ", item.f)
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
            velocities = []
            g = []
            h = []
            f = []
            direccion = []
            current = current_node
            while current is not None:
                path.append(current.position)
                velocities.append(current.velocity)  # 💡 Añadimos la velocidad efectiva aquí
                g.append(current.g)
                h.append(current.h)
                f.append(current.f)
                direccion.append(current.direction)
                current = current.parent
            g = [round(float(x), 3) for x in g]
            h = [round(float(x), 3) for x in h]
            f = [round(float(x), 3) for x in f]
            return path[::-1], expanded_nodes, generated_nodes, velocities[::-1], g[::-1], h[::-1], f[::-1], direccion[::-1] # Se retorna el camino invertido ([::-1]), ya que fue construido desde el final al inicio.

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

            # Create the f, g, and h values ----------------------------------------------------------------------------------------------------------------------

            ##variacion para incluir la velocidad y direccion del viento + velocidad del barco
            #VIENTO
            v_viento = velocidad_viento[node_position[0]][node_position[1]] 
            d_viento = direccion_viento[node_position[0]][node_position[1]]

            #direccion real
            angulo_viento = d_viento + 180
            print("angulo viento real: ", angulo_viento)

            #angulo para las ecuaciones
            if angulo_viento <= 90:
                angulo_viento = 90 - angulo_viento
            if angulo_viento > 90 and angulo_viento <= 180:
                angulo_viento = -(angulo_viento - 90)
            if angulo_viento > 180 and angulo_viento <= 270:
                angulo_viento = -(angulo_viento - 90)
            if angulo_viento > 270:
                angulo_viento = 360 - angulo_viento + 90
             #-> ya tendriamos el angulo
            print("angulo viento para el calculo: ", angulo_viento)

            #BARCO
            v_barco = current_node.velocity     #TIENE QUE IR CAMBIANDO, en new_node se actualiza
            print("velocidad barco: ", v_barco)

            if current_node.direction == 'N':
                angulo_barco = 90
            if current_node.direction == 'S':
                angulo_barco = -90
            if current_node.direction == 'E':
                angulo_barco = 0
            if current_node.direction == 'W':
                angulo_barco = 180
            if current_node.direction == 'NW':
                angulo_barco = 135
            if current_node.direction == 'NE':
                angulo_barco = 45
            if current_node.direction == 'SW':
                angulo_barco = -135
            if current_node.direction == 'SE':
                angulo_barco = -45
            
            print("angulo barco: ", angulo_barco)

            #calculos
            tolerancia = 1e-10

            vx_viento = v_viento * np.cos(np.radians(angulo_viento))
            # Redondear si está dentro del umbral
            if abs(vx_viento) < tolerancia:
                vx_viento = 0.0
            print("vx viento: ", vx_viento)

            vy_viento = v_viento * np.sin(np.radians(angulo_viento))
            if abs(vy_viento) < tolerancia:
                vy_viento = 0.0
            print("vy viento: ", vy_viento)

            vx_barco = v_barco * np.cos(np.radians(angulo_barco))
            if abs(vx_barco) < tolerancia:
                vx_barco = 0.0
            print("vx barco: ", vx_barco)

            vy_barco = v_barco * np.sin(np.radians(angulo_barco))
            if abs(vy_barco) < tolerancia:
                vy_barco = 0.0
            print("vy barco: ", vy_barco)

            vx_resultante = vx_viento + vx_barco
            print("vx resultante: ", vx_resultante)
            vy_resultante = vy_viento + vy_barco
            print("vy resultante: ", vy_resultante)

            v_resultante = np.sqrt(vx_resultante**2 + vy_resultante**2) 
            print("v resultante: ", v_resultante)

            if angulo_barco == angulo_viento or vx_resultante == 0:
                angulo_resultante = angulo_barco
            else:
                angulo_resultante = np.arctan(vy_resultante / vx_resultante)
                angulo_resultante = np.degrees(angulo_resultante)

            
            print("angulo resultante: ", angulo_resultante)

            #velocidad effectiva
            v_eff = v_resultante * np.cos(np.radians(angulo_barco - angulo_resultante))
            print("v efectiva: ", v_eff)

            new_node.velocity = v_eff #se actualiza la velocidad del barco
            print("velocidad barco nueva: ", new_node.velocity)
            

            new_node.g = (current_node.g + 1) / v_eff                             #Costo desde el inicio hasta este nodo (+1 respecto al padre).
            print("g: ", new_node.g)
            new_node.h = (
                (new_node.position[0] - end_node.position[0]) ** 2 +    #Heurística: distancia euclidiana cuadrada al objetivo.
                (new_node.position[1] - end_node.position[1]) ** 2
            )
            new_node.h = new_node.h / v_eff
            print("h: ", new_node.h)

            new_node.f = new_node.g + new_node.h
            print("f: ", new_node.f)
            
            

            #-------------------------------------------------------------------------------------------------------------------------------------------------

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

        #ooo += 1
        #if ooo == 3:
        #    break

    return None, expanded_nodes, generated_nodes, None


def visualize_maze_with_generated(maze, path, expanded_nodes, generated_nodes):
    # Crear una copia de la matriz del laberinto
    visual_maze = np.zeros((len(maze), len(maze[0]), 3), dtype=np.float32)

    # Asignar colores a cada celda
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:  # Pared -> Negro
                visual_maze[i, j] = [0, 0, 0]
            elif maze[i][j] == 2:  # Camino -> Gris
                visual_maze[i, j] = [0.5, 0.5, 0.5]
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
    plt.title("viento 5m/s, barco 10 m/s, viento al Oeste")
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

    # Velocidad del viento en cada celda m/s???
    velocidad_viento = [
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    ]

    # Primera prueba es al N=0º, pero como la matriz es de donde viene el viento, es al reves y despues se le suma 180º
    direccion_viento = [
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180],
        [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
    ]

    start = (19,1)
    end = (1,19)
    start_direction = 'N' #'S'
    start_velocity = 10 # m/s????

    maze_holgura = agregar_holgura(maze)

    path, expanded_nodes, generated_nodes, velocities, g, h, f, direccion_barco = astar_with_generated_nodes(maze_holgura, velocidad_viento, direccion_viento, start, end, start_direction, start_velocity)

    if path is None:
        print("No se encontró un camino válido desde el inicio hasta el objetivo.")
        return

    print("Path:", path)
    print("Velocities:", velocities)
    print("g:", g)
    print("h:", h)
    print("f:", f)
    print("Dirección del barco:", direccion_barco)
    print("Expanded Nodes:", expanded_nodes)
    print(f"Total Expanded Nodes: {len(expanded_nodes)}")

    print("Generated Nodes:", generated_nodes)
    print(f"Total Generated Nodes: {len(generated_nodes)}")

    
    # Verificar si los nodos expandidos coinciden con el camino solución
    verify_expanded_vs_solution(path, expanded_nodes)

    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - started:.6f} segundos")


    #---------------------------------------------------------------------------------------------------------------------------------------
    # añadir un indice
    # Construcción del diccionario de resultados
    resultados = {
        "Path": [str(path)],
        "Expanded Nodes": [str(expanded_nodes)],
        "Total Expanded Nodes": [len(expanded_nodes)],
        "Generated Nodes": [str(generated_nodes)],
        "Total Generated Nodes": [len(generated_nodes)],
        "Tiempo de ejecución (s)": [round(end - started, 6)]
    }

    # Convertimos a DataFrame
    df = pd.DataFrame(resultados)

    # Crear la carpeta si no existe
    carpeta = "datos_resultados"
    os.makedirs(carpeta, exist_ok=True)

    # Nombre del archivo con ruta
    nombre_archivo = os.path.join(carpeta, "resultados_busqueda.xlsx")

    try:
        # Intentamos agregar a un archivo existente si ya hay uno
       # Después de crear df como antes...
        with pd.ExcelWriter(nombre_archivo, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer: #con overlay se van añadiendo cosas nuevas sin modificar lo que ya estaba
            hoja = writer.sheets.get("Resultados")
            startrow = hoja.max_row if hoja else 0
            df.to_excel(writer, sheet_name="Resultados", index=False, startrow=startrow, header=not hoja)

    except FileNotFoundError:
        # Si no existe, lo creamos desde cero
        df.to_excel(nombre_archivo, sheet_name="Resultados", index=False)

    print("✅ Resultados guardados en Excel.")

    # Visualizar el laberinto con la solución, nodos expandidos y generados
    visualize_maze_with_generated(maze_holgura, path, expanded_nodes, generated_nodes)


if __name__ == '__main__':
    
    main()
    
