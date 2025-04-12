
import numpy as np


d_viento = 300

#direccion real
angulo_viento = d_viento + 180

#angulo para las ecuaciones
if angulo_viento < 90:
    angulo_viento = 90 - angulo_viento
if angulo_viento > 90 and angulo_viento < 180:
    angulo_viento = -(angulo_viento - 90)
if angulo_viento > 180 and angulo_viento < 270:
    angulo_viento = -(angulo_viento - 90)
if angulo_viento > 270:
    angulo_viento = 360 - angulo_viento + 90

print(angulo_viento)

vx_viento = np.cos(np.radians(90))

print(vx_viento)

v_resultante = np.sqrt(9.191**2 + (-4.949)**2)

print(v_resultante) 