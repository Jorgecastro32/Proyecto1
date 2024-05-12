from sklearn.linear_model import LinearRegression
import pandas as pd
from pulp import *

# Creamos un dataframe con datos. Orden: La Paz, Gregorio Marañon, 12 de Octubre, Ramón y Cajal
datos = pd.DataFrame({
    'camas': [966, 1140, 1300, 892],   
    'personal medico': [2038, 1222, 1714, 2295],
    'demanda': [684, 741, 837, 442],
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
w3 = modelo.coef_[0][2]  # Peso de la Demanda
intercepto = modelo.intercept_[0]

# Imprimimos coeficientes y término de intercepción
print("Coeficientes:\n \t w1=", w1, "\n \t w2=", w2, '\n \t w3=', w3)
print("Término de intercepción:", intercepto)  

#PROGRAMACIÓN LINEAL. LIBRERÍA PULP.
#Variables
modelo = LpProblem("Administras gastos de camas y médicos", sense= LpMaximize)
camas_disponibles= LpVariable("Camas utilizadas", lowBound=0, cat="Integer")
camas_liberadas=LpVariable("Camas libres", lowBound=0, cat="Integer")
medicos_trabajando= LpVariable("Médicos trabajando", lowBound=0, cat="Integer")
medicos_libres=LpVariable("Médicos libres", lowBound=0, cat="Integer")


#Pedimos datos al usuario
total_camas = int(input("Ingrese el número total de camas en el hospital: ")) #Indicamos en la terminal el número de camas del hospital
total_medicos = int(input("Ingrese el número total de medicos en el hospital: ")) #Indicamos en la terminal el número de médicos del hospital
presupuesto=int(input("¿Cuál es el presupuesto del hospital?")) #Presupuesto del hospital de urgencias ZENDAL. Habría que encontrar el presupuesto del hospital La Paz
demanda=int(input("¿Cuál es la demanda del hospital?"))
camas_necesarias=demanda
turno_medicos = (total_medicos*31)/100 #El número de médicos trabajando en urgencias es del 31%)


#FUNCIÓN A OPTIMIZAR. Cada cama disminuye 0.0142... uds de tiempo y cada medico disminuye 0.036.... uds de tiempo.
modelo += camas_disponibles*int(w1) + medicos_trabajando*int(w2) - demanda*int(w3)

#Restricciones
modelo += medicos_trabajando*2694 + camas_disponibles*5141 <= presupuesto  # Se desembolsan 5141€ por cada cama en uso y 2694€ por cada médico trabajando. El gasto no puede sobrepasar el presupuesto
modelo += camas_liberadas + camas_disponibles == total_camas 
modelo += medicos_libres + medicos_trabajando == turno_medicos
modelo += camas_disponibles>=camas_necesarias  #Las camas disponibles deben ser un número mayor que las camas necesarias para cubrir la demanda
modelo += 5*medicos_trabajando <= camas_disponibles  #Cada médico cubre 3 camas

#Resolvemos el la función objetivo
modelo.solve()

#Imprimimos por pantalla los resultados que nos interesan
print("Tenemos un presupuesto de:", int(presupuesto), "€")
print("\t Encontramos {} camas libres".format(int(camas_liberadas.varValue)))
print("\t Encontramos {} camas disponibles por las que se desembolsan {}".format(int(camas_disponibles.varValue), int(camas_disponibles.varValue*5141)))
print("\t Necesitamos {} camas para cubrir la demanda del hospital en este momento".format(int(camas_necesarias)))

#Posibles errores
#Si la demanda es demasiado grande y no disponemos de tantas camas en el hospital para cubrirla
if camas_necesarias>camas_disponibles.varValue:
    print("ERROR. No disponemos de tantas camas para controlar esta demanda")
    sys.exit() #Salimos del programa si hay error
else:  #Si las camas necesarias no son tantas como las camas disponibles, ajustamos las camas disponibles para ahorrar presupuesto
    camas_disponibles=camas_necesarias
    medicos_trabajando=camas_necesarias/5
    print("\t\nVamos a utilizar {} camas y {} médicos. Podemos liberar {} médicos".format(int(camas_necesarias), int(medicos_trabajando), int(medicos_libres.varValue)))

#Limitación presupuestaria.
if int(medicos_trabajando*2694) + int(camas_disponibles*5141) > presupuesto:
    print("ERROR. Hay pacientes que no pueden ser atendidos de forma correcta por la limitación de presupuesto.") #Sino disponemos de presupuesto, imprime error
    sys.exit()
else:
    presupuesto_utilizado = int(medicos_trabajando*2694 + camas_disponibles*5141)
    presupuesto_sobrante = int(presupuesto - presupuesto_utilizado)
    print("\tPresupuesto utilizado:", presupuesto_utilizado, "€\n \tPresupuesto sobrante:", presupuesto_sobrante, "€")


# ¿Cómo podemos distribuir el presupuesto sobrante de la mejor manera posible?
# Variables
modelo = LpProblem("Administras gastos de camas y médicos", sense=LpMaximize)
camas_nuevas = LpVariable("Camas nuevas", lowBound=0, cat="Integer")
medicos_nuevos = LpVariable("Médicos nuevos", lowBound=0, cat="Integer")

# Función objetivo
modelo += camas_nuevas + medicos_nuevos

# Restricciones
modelo += medicos_nuevos * 2694 + camas_nuevas * 5141 <= presupuesto_sobrante  
modelo += 5 * medicos_nuevos <= camas_nuevas  

# Resolvemos la función objetivo
modelo.solve()

# Imprimimos por pantalla los resultados que nos interesan
print("Tenemos un presupuesto sobrante de:", int(presupuesto_sobrante), "€")
print("\t Encontramos {} camas nuevas y {} médicos nuevos".format(int(camas_nuevas.varValue), int(medicos_nuevos.varValue)))
print("\t Desembolsamos {} € por las nuevas camas y {} € por los nuevos médicos".format(int(camas_nuevas.varValue * 5141), int(medicos_nuevos.varValue * 2694)))

# Tiempo disminuido
tiempo_de_espera_disminuido = camas_nuevas.varValue * 0.02429120787872738 + medicos_nuevos.varValue * 0.03500869073653192
print("\nDisminuiríamos el tiempo de espera en", tiempo_de_espera_disminuido, "minutos")