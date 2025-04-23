import numpy as np

def agregar_holgura(mapa):
    mapa = np.array(mapa)
    filas, columnas = mapa.shape
    resultado = mapa.copy()

    for i in range(filas):
        for j in range(columnas):
            if mapa[i, j] == 1:
                # Revisamos todas las posiciones vecinas (incluso diagonales)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < filas and 0 <= nj < columnas:
                            if resultado[ni, nj] == 0:
                                resultado[ni, nj] = 2
                                
    return resultado.tolist()


