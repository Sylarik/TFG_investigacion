import time


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

# Direcciones posibles (8 movimientos: verticales, horizontales y diagonales)
MOVEMENTS = [
    (0, -1), (0, 1), (-1, 0), (1, 0),
    (-1, -1), (-1, 1), (1, -1), (1, 1)
]

def a_star_pathfinding(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize both open and closed list
    open_list = [start_node]
    closed_list = []

    # Loop until you find the end
    while open_list:

        # Get the current node
        current_node = open_list[0]
        for node in open_list:
            if node.f < current_node.f:
                current_node = node
        open_list.remove(current_node)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            temp = current_node
            while temp:
                path.append(temp.position)
                temp = temp.parent
            return path[::-1] #devulve el camino en orden inverso

        # Generamos vecinos
        for dx, dy in MOVEMENTS:

            new_position = (current_node.position[0] + dx, current_node.position[1] + dy)

            # Validar límites
            if not (0 <= new_position[0] < len(maze)) or not (0 <= new_position[1] < len(maze[0])):
                continue

            # Si es obstáculo, lo saltamos
            if maze[new_position[0]][new_position[1]] != 0:
                continue

            new_node = Node(current_node, new_position)

            if new_node in closed_list:
                continue

            # Cálculo de costes
            new_node.g = current_node.g + 1
            dx = abs(new_node.position[0] - end_node.position[0])
            dy = abs(new_node.position[1] - end_node.position[1])
            new_node.h = dx + dy  # Distancia Manhattan
            new_node.f = new_node.g + new_node.h

#-------------------------------------------------------------------------------------------------------------------------------

            # Comprobar si el vecino ya está en open_list con un mejor g
            for existing_node in open_list:
                if new_node == existing_node and new_node.g >= existing_node.g:
                    break
            else:
                open_list.append(new_node)  # No había ninguno igual, lo añadimos

                with open('output6.txt', 'a') as file:  # 'a' para agregar al archivo sin sobrescribir
                    for opem_node in open_list:
                        file.write(f"{opem_node.position}\n")
            #si pongo esto chatgpt me dice que esta mal:
            # for existing_node in open_list:
            #     if new_node == existing_node and new_node.g >= existing_node.g:
            #         continue  # Ya hay una versión mejor, salimos del bucle
            #  
            # open_list.append(new_node)
            #   
            # 
            # ---
            # for existing_node in open_list:
            #     if new_node == existing_node:
            #         if new_node.g < existing_node.g:
            #             open_list.remove(existing_node)  # Quitamos el peor
            #             open_list.append(new_node)      # Añadimos el mejor
            #         break
            # else:
            #     open_list.append(new_node)  # No había ninguno igual, lo añadimos
        
#-------------------------------------------------------------------------------------------------------------------------------
            '''
            if any(existing for existing in open_list if new_node == existing and new_node.g >= existing.g):
                continue  # ❗ Aquí el continue sí salta toda la iteración del bucle de vecinos
            
            open_list.append(new_node)
            '''

    return None  # No se encontró ruta


def main():
    started = time.perf_counter()
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (1,0)
    end = (6,4)

    path = a_star_pathfinding(maze, start, end)
    end = time.perf_counter()
    print(f"Tiempo de ejecución: {end - started:.6f} segundos")
    print(path)


if __name__ == '__main__':
    main()


#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2