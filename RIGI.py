# -*- coding: utf-8 -*-
"""Copia de Tesis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H0bPmi5Opj0v0JMuUv2jRWlgSeTmLdiL
"""

import pandas as pd
import sympy as sp
import numpy as np
from scipy.optimize import fsolve
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""Definimos las variabes y le damos valores a los parámetros que necesitemos."""

q = sp.symbols('q')
b = sp.symbols('b')
a = 100
a0 = 5
a1 = 2.5
a2 = 1.5
a3 = sp.symbols('a3')
n = sp.symbols('n')
qL = sp.symbols('qL')
qS = sp.symbols('qS')

"""# **Stackelberg con 2 Firmas**"""

ingreso_S_2 = (a-b*(qL+qS))*qS

costo_S_2 = a3*qS**3 + a2*qS**2 + a1*qS + a0

beneficio_S_2 = ingreso_S_2 - costo_S_2
beneficio_S_2

beneficio_S_2_D = sp.diff(beneficio_S_2,qS)
beneficio_S_2_D

f_reaccion_S = sp.solve(beneficio_S_2_D, qS)
print(f_reaccion_S[0])
print(f_reaccion_S[1])

f_reaccion_S_1 = f_reaccion_S[1]
f_reaccion_S_1

f_reaccion_S_0 = f_reaccion_S[0]
f_reaccion_S_0

ingreso_L_2 = (a-b*(qS+qL))*qL
costo_L_2 = a3*qL**3 + a2*qL**2 + a1*qL + a0
beneficio_L_2 = ingreso_L_2 - costo_L_2
beneficio_L_2

beneficio_L_2_reemp_reaccion_1 = beneficio_L_2.subs('qS',f_reaccion_S_1)
beneficio_L_2_reemp_reaccion_1

beneficio_L_2_reemp_reaccion_0 = beneficio_L_2.subs('qS',f_reaccion_S_0)
beneficio_L_2_reemp_reaccion_0

beneficio_L_2_reemp_D_reaccion_0 = sp.diff(beneficio_L_2_reemp_reaccion_0, qL)
beneficio_L_2_reemp_D_reaccion_0

beneficio_L_2_reemp_D_reaccion_1 = sp.diff(beneficio_L_2_reemp_reaccion_1, qL)
beneficio_L_2_reemp_D_reaccion_1

beneficio_L_2_reemp_DD_reaccion_0 = sp.diff(beneficio_L_2_reemp_D_reaccion_0, qL)
beneficio_L_2_reemp_DD_reaccion_0

beneficio_L_2_reemp_DD_reaccion_1 = sp.diff(beneficio_L_2_reemp_D_reaccion_1, qL)
beneficio_L_2_reemp_DD_reaccion_1

"""Vamos a hacer un bucle donde le vamos a ir dando valores a `a3` entre 0.2 y 6, y a su vez a `b` entre 0.2 y 4.




"""

f_reaccion_S_1_derivada = sp.diff(f_reaccion_S_1, qL)
f_reaccion_S_1_derivada

resultados_reaccion_1 = []

for a3 in np.arange(0.2, 3, 0.2):

    for b in np.arange(10, 200, 10):

      beneficio_L_2_reemp_D_mod = beneficio_L_2_reemp_D_reaccion_1.subs('a3', a3).subs('b', b)
      soluciones = sp.solve(beneficio_L_2_reemp_D_mod, qL)
      #print(soluciones)


      for solucion in soluciones:

        beneficio_L_2_reemp_DD_mod = beneficio_L_2_reemp_DD_reaccion_1.subs('a3', a3).subs('b', b).subs('qL',solucion)

        if solucion < 0 or solucion:
          soluciones.remove(solucion)

        elif solucion.is_real == False:
          soluciones.remove(solucion)

        elif beneficio_L_2_reemp_DD_mod > 0:
          soluciones.remove(solucion)

      cantidades_segudiora = []
      beneficios_lider = []
      beneficios_segudiora = []

      for sol in soluciones:
        q_seguidora = f_reaccion_S_1.subs('a3', a3).subs('b', b).subs('qL',sol)
        cantidades_segudiora.append(q_seguidora)
        beneficio_lider = beneficio_L_2_reemp_reaccion_1.subs('a3', a3).subs('b', b).subs('qL',sol)
        beneficios_lider.append(beneficio_lider)
        beneficio_segudiora = beneficio_S_2.subs('a3', a3).subs('b', b).subs('qL',sol).subs('qS', q_seguidora)
        beneficios_segudiora.append(beneficio_segudiora)

      fila_resultado = {'valor_a3': a3, 'valor_b': b}

      for idx, cant_lider in enumerate(soluciones):
        fila_resultado[f'q_lider{idx + 1}'] = cant_lider

      for idx, cant_seguidora in enumerate(cantidades_segudiora):
        fila_resultado[f'q_segudiora{idx + 1}'] = cant_seguidora

      for idx, benef_lider in enumerate(beneficios_lider):
        fila_resultado[f'beneficio_lider{idx + 1}'] = benef_lider

      for idx, benef_seguidora in enumerate(beneficios_segudiora):
        fila_resultado[f'beneficio_seguidora{idx + 1}'] = benef_seguidora

      resultados_reaccion_1.append(fila_resultado)

df_resultados_reaccion_1 = pd.DataFrame(resultados_reaccion_1)

df_resultados_reaccion_1.head(30)

df_resultados_reaccion_1.plot(kind = 'scatter', x = 'valor_a3', y = 'q_lider1')

df_resultados_reaccion_1.plot(kind = 'scatter', x = 'valor_b', y = 'q_lider1')

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(df_resultados_reaccion_1['valor_a3'], df_resultados_reaccion_1['valor_b'], df_resultados_reaccion_1['q_lider1'], c=df_resultados_reaccion_1['q_lider1'], cmap='viridis')

ax.set_xlabel('valor_a3')
ax.set_ylabel('valor_b')
ax.set_zlabel('q_lider1')

plt.show()

resultados_reaccion_1_uno = []

for a3 in np.arange(0.1, 1, 0.1):

    for b in np.arange(100, 200, 25):

      beneficio_L_2_reemp_D_mod = beneficio_L_2_reemp_D_reaccion_1.subs('a3', a3).subs('b', b)
      soluciones = sp.solve(beneficio_L_2_reemp_D_mod, qL)
      #print(soluciones)


      for solucion in soluciones:

        beneficio_L_2_reemp_DD_mod = beneficio_L_2_reemp_DD_reaccion_1.subs('a3', a3).subs('b', b).subs('qL',solucion)

        if solucion < 0 or solucion:
          soluciones.remove(solucion)

        elif solucion.is_real == False:
          soluciones.remove(solucion)

        elif beneficio_L_2_reemp_DD_mod > 0:
          soluciones.remove(solucion)

      cantidades_segudiora = []
      beneficios_lider = []
      beneficios_segudiora = []

      for sol in soluciones:
        q_seguidora = f_reaccion_S_1.subs('a3', a3).subs('b', b).subs('qL',sol)
        cantidades_segudiora.append(q_seguidora)
        beneficio_lider = beneficio_L_2_reemp_reaccion_1.subs('a3', a3).subs('b', b).subs('qL',sol)
        beneficios_lider.append(beneficio_lider)
        beneficio_segudiora = beneficio_S_2.subs('a3', a3).subs('b', b).subs('qL',sol).subs('qS', q_seguidora)
        beneficios_segudiora.append(beneficio_segudiora)

      fila_resultado = {'valor_a3': a3, 'valor_b': b}

      for idx, cant_lider in enumerate(soluciones):
        fila_resultado[f'q_lider{idx + 1}'] = cant_lider

      for idx, cant_seguidora in enumerate(cantidades_segudiora):
        fila_resultado[f'q_segudiora{idx + 1}'] = cant_seguidora

      for idx, benef_lider in enumerate(beneficios_lider):
        fila_resultado[f'beneficio_lider{idx + 1}'] = benef_lider

      for idx, benef_seguidora in enumerate(beneficios_segudiora):
        fila_resultado[f'beneficio_seguidora{idx + 1}'] = benef_seguidora

      resultados_reaccion_1_uno.append(fila_resultado)

df_resultados_reaccion_1_uno = pd.DataFrame(resultados_reaccion_1_uno)

df_resultados_reaccion_1_uno.head(30)