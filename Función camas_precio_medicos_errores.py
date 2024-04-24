from pulp import *
#Variables
modelo = LpProblem("Administras gastos de camas", sense= LpMaximize)
camas_utilizadas= LpVariable("Camas utilizadas", lowBound=0, cat="Integer")
camas_liberadas=LpVariable("Camas libres", lowBound=0, cat="Integer")
medicos_trabajando= LpVariable("Médicos trabajando", lowBound=0, cat="Integer")
medicos_libres=LpVariable("Médicos libres", lowBound=0, cat="Integer")

presupuesto=6152634  #Presupuesto del hospital de urgencias ZENDAL. Habría que encontrar el presupuesto del hospital La Paz
pacientes=500
#Función a optimizar. Se desembolsan 5141€ por cada cama en uso y 3763€ por cada cama libre
modelo += camas_utilizadas*5141 + camas_liberadas*3763

#Restricciones
modelo += camas_liberadas*3763 + camas_utilizadas*5141 <= presupuesto  #El gasto en camas debe ser menor al presupuesto
modelo += camas_liberadas + camas_utilizadas == 1308 #El número de camas == 1308
modelo += medicos_libres + medicos_trabajando == 978 #El número de médicos trabajando es de 978
modelo += (pacientes/3) <= medicos_trabajando #Necesitamos un médico para cada 3 camas

#Posibles errores sino tenemos suficiente presupuesto en camas o en médicos para cubrir al número de pacientes
if pacientes>int(camas_utilizadas):
    #print("ERROR. No tenemos suficiente presupuesto en camas para cubrir a", pacientes, "pacientes")

if medicos_trabajando<pacientes/3:
    #print("ERROR. No tenemos suficiente presupuesto en médicos para cubrir a", pacientes, "pacientes")

modelo.solve()

#Imprimimos por pantalla los resultados que nos interesan
print("Tenemos un presupuesto destinado a camas de:", int(presupuesto), "€")
print("\t Encontramos {} camas libres por las que se desembolsan {}".format(int(camas_liberadas.varValue), int(camas_liberadas.varValue*3763)))
print("\t Encontramos {} camas en uso por las que se desembolsan {}".format(int(camas_utilizadas.varValue), int(camas_utilizadas.varValue*5141)))
print("\t Necesitamos {} médicos para cubrir las camas en uso. Podemos liberar a {} médicos.".format(int(medicos_trabajando.varValue), int(medicos_libres.varValue)))
