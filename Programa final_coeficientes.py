from sklearn.linear_model import LinearRegression
import pandas as pd
from pulp import *

# Creamos un dataframe con datos. Orden: La Paz, Gregorio Marañon, 12 de Octubre, Ramón y Cajal
datos = pd.DataFrame({
    'camas': [966, 1140, 1300, 892],   
    'personal medico': [2038, 1222, 1714, 2295],
    'demanda': []
    'tiempo': [90, 115, 95, 80]
})

# Variables independientes
X = datos[['camas', 'personal medico', 'demanda']]

# Variable dependiente
y = datos[['tiempo']]

# Ajustamos el modelo de regresión lineal
modelo = LinearRegression()
modelo.fit(X, y)

# Obtenemos coeficientes y término de intercepción
w1 = modelo.coef_[0][0]  # Peso de las camas
w2 = modelo.coef_[0][1]  # Peso de los médicos
w3 = modelo.coef_[0][2]  # Demanda
intercepto = modelo.intercept_[0]

# Imprimimos coeficientes y término de intercepción
print("Coeficientes:\n \t w1=", w1, "\n \t w2=", w2, '\n \t w3=', w3)
print("Término de intercepción:", intercepto)  

#PROGRAMACIÓN LINEAL. LIBRERÍA PULP.
# Creamos el modelo de programación lineal
modelo_lp = LpProblem("Tiempos de espera en función de camas, médicos y demanda", sense=LpMinimize)

# Definimos las variables de decisión
camas = LpVariable("Camas utilizadas", lowBound=0, cat="Integer")
medicos = LpVariable("Médicos utilizados", lowBound=0, cat="Integer")
demanda = LpVariable("Demanda", lowBound=0, cat="Integer")

# Definimos la función objetivo
modelo_lp += ( w1 * camas + w2 * medicos - w3 * demanda)

# Restricciones. Nuestras restricciones están relacionadas con el presupuesto
#modelo_lp += (3037 * camas + 2696 * medicos)<=presupuesto 

# Resolvemos el modelo
modelo_lp.solve()

# Imprimimos los resultados
print("\tEncontramos {} camas".format(int(camas.varValue)))
print("\tEncontramos {} médicos".format(int(medicos.varValue)))


