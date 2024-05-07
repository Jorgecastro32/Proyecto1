from sklearn.linear_model import LinearRegression
import pandas as pd
from pulp import *

# Creamos un dataframe con datos. Orden: La Paz, Gregorio Marañon, 12 de Octubre, Ramón y Cajal
datos = pd.DataFrame({
    'camas': [966, 1140, 1300, 892],   
    'personal medico': [2038, 1222, 1714, 2295],
    'tiempo': [90, 115, 95, 80]
})

# Variables independientes
X = datos[['camas', 'personal medico']]

# Variable dependiente
y = datos[['tiempo']]

# Ajustamos el modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X, y)

# Obtenemos coeficientes y término de intercepción
w1 = modelo.coef_[0][0]  # Peso de las camas
w2 = modelo.coef_[0][1]  # Peso de los médicos
intercepto = modelo.intercept_[0]

# Imprimimos coeficientes y término de intercepción
print("Coeficientes:\n \t w1=", w1, "\n \t w2=", w2)
print("Término de intercepción:", intercepto)  #El intercepto representa el valor de y cuando todas las variables independientes son cero. 
#En este contexto, podría interpretarse como el tiempo de respuesta esperado si un hospital no tuviera camas ni personal médico. 
#Los coeficientes (w1 y w2) representan el cambio esperado en y por cada unidad de cambio en las variables independientes X1 (camas) y X2 (personal médico), respectivamente.




