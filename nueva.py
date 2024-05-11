from pulp import *
#Variables
modelo = LpProblem("Administras gastos de camas", sense= LpMaximize)
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
modelo += camas_disponibles*0.014277367794469711 + medicos_trabajando*0.03609546749383334 - demanda*0.004572269627625781

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
print("\t Necesitamos {} médicos para cubrir las camas disponibles. Podemos liberar a {} médicos.".format(int(medicos_trabajando.varValue), int(medicos_libres.varValue)))
print("\t Necesitamos {} camas para cubrir la demanda del hospital en este momento".format(int(camas_necesarias)))

#Posibles errores
#Si la demanda es demasiado grande y no disponemos de tantas camas en el hospital para cubrirla
if camas_necesarias>camas_disponibles.varValue:
    print("ERROR. No disponemos de tantas camas para controlar esta demanda")
    sys.exit() #Salimos del programa si hay error
else:  #Si las camas necesarias no son tantas como las camas disponibles, ajustamos las camas disponibles para ahorrar presupuesto
    camas_disponibles=camas_necesarias
    medicos_trabajando=camas_necesarias/5
    print("\tVamos a utilizar {} camas y {} médicos".format(int(camas_necesarias), int(medicos_trabajando)))

#Limitación presupuestaria.
if int(medicos_trabajando*2694) + int(camas_disponibles*5141) > presupuesto:
    print("ERROR. Hay pacientes que no pueden ser atendidos de forma correcta por la limitación de presupuesto.") #Sino disponemos de presupuesto, imprime error
else:
    presupuesto_utilizado = int(medicos_trabajando*2694 + camas_disponibles*5141)
    presupuesto_sobrante = int(presupuesto - presupuesto_utilizado)
    print("\tPresupuesto utilizado:", presupuesto_utilizado, "€\n \tPresupuesto sobrante:", presupuesto_sobrante, "€")


