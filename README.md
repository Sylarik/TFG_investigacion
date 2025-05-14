

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
