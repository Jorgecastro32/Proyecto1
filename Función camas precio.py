from pulp import *
#Variables
modelo = LpProblem("Administras gastos de camas", sense= LpMaximize)
camas_utilizadas= LpVariable("Camas utilizadas", lowBound=0, cat="Integer")
camas_liberadas=LpVariable("Camas libres", lowBound=0, cat="Integer")
presupuesto=6152634  #Presupuesto del hospital de urgencias ZENDAL. Habría que encontrar el presupuesto del hospital La Paz

#Función a optimizar. Se desembolsan 5141€ por cada cama en uso y 3763€ por cada cama libre
modelo += camas_utilizadas*5141 + camas_liberadas*3763

#Restricciones
modelo += camas_liberadas*3763 + camas_utilizadas*5141 <= presupuesto  #El gasto en camas debe ser menor al presupuesto
modelo += camas_liberadas + camas_utilizadas == 1308 #El número de camas == 100
modelo.solve()

#Imprimimos por pantalla los resultados que nos interesan
print("Tenemos un presupuesto destinado a camas de:", int(presupuesto), "€")
print("\t Encontramos {} camas libres por las que se desembolsan {}".format(int(camas_liberadas.varValue), int(camas_liberadas.varValue*3763)))
print("\t Encontramos {} camas en uso por las que se desembolsan {}".format(int(camas_utilizadas.varValue), int(camas_utilizadas.varValue*5141)))
