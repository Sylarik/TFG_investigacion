
todas las cooordenadas en el codigo estan como (Y,X) no (x,y)

ruta

modelo_internet
    - la base del proyecto
    - lo unico que he cambiado es el mapa y el comienzo y final
    - el mapa lo he sacado de este paper "Mathematical Problems in Engineering - 2021 - Chen - Research on Ship Meteorological Route Based on A‐Star Algorithm"

nodos_expandidos
    - te dice el path y los nodos expandidos
    ![Descripción de la imagen](imagenes\nodos_expandidos.png)

color
    - lo mismo que nodos_expandidos.py pero se añade una funcion para ver los colores -> hacer funcion a parte?
    - lo guarda como png (la imagen del mapa)
    ![Descripción de la imagen](imagenes\img_color.png)


generados
    - se añade que guarde tmb los nodos generados + funcion para ver si coinciden los generados con los expandidos (xq en un mapa si coincidia)
    - esta el tiempo de ejecucion

    start = (1,0)
    end = (6,4)
![Descripción de la imagen](imagenes\img_generados.png)

    start = (1,0)
    end = (5,4)
![Descripción de la imagen](imagenes\img_generados2.png)

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

angulos
![Descripción de la imagen](imagenes\img_angulos.png)

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


angulos.py
    - está el mapa de barcelona-islas
    - se aplica lo de que solo tiene en cuenta las tres casillas que tiene en frente


con_viento.py
    - en este voy a probar a meter direccion y velocidad del viento.
    - lo voy a probar con lo del paper.

generador_multiple_datos.py
    - se añade (a con_viento.py) un bucle con distintos valores para los datos

holgura.py 
    - solo funcion de holgura -> funciona



PROBLEMAS:
    1. a veces tenia en la parte de abajo de lo de calcular el anugulo un 0, entonces daba indefinido
        sol: eso me pasaba cuando iba la direccion de barco y del viento en el mismo eje, entonces puse una restriccion
    2. una cosa me salia negativo
    3. lo de que como no estaba en radianes me daba unos numeros raros al calcular los angulos

    4. el codigo original del articulo tiene mal lo de append ya que guarda todos los nodos (el continue no funciona)
        sol: he cambiado en mi codigo con una funcion con un break -> ver los outputs.txt

        output.txt -> original con el bucle
        output2.txt -> original son el bucle -> hace lo mismo -> el bucle no hacia nada
        output3.ttx -> el mio con el break -> añade menos nodos
        output4.txt -> el mio con lo de que se elimine el nodo si hay uno con menor g -> no hace nada
        output5.txt -> el 4 pero con otro mapa
        output6. txt -> el 3 pero con otro mapa -> es igual que el 5 -> no hace nada lo de elinar el nodo?


    5. Distancia euclidiana o la de manhatan??
        sol: mejor la euclidiana porque tiene en cuenta las diagonales (añadir foto google)

        path: [(2, 1), (3, 2), (4, 2), (5, 2), (6, 3), (7, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (12, 14)]
        con manhatan: Heuristics: [0, 21, 20, 19, 17, 15, 13, 12, 11, 10, 9, 7, 5, 3, 1, 0]
        con euclidiana: Heuristics: [0, 15.0, 14.422205101855956, 13.892443989449804, 12.529964086141668, 11.180339887498949, 9.848857801796104, 8.94427190999916, 8.06225774829855, 7.211102550927978, 6.4031242374328485, 5.0, 3.605551275463989, 2.23606797749979, 1.0, 0.0]

        -> el path en los dos cosas
