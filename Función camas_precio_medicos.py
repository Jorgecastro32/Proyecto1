from pulp import *
#Variables
modelo = LpProblem("Administras gastos de camas", sense= LpMaximize)
camas_utilizadas= LpVariable("Camas utilizadas", lowBound=0, cat="Integer")
camas_liberadas=LpVariable("Camas libres", lowBound=0, cat="Integer")
medicos_trabajando= LpVariable("Médicos trabajando", lowBound=0, cat="Integer")
medicos_libres=LpVariable("Médicos libres", lowBound=0, cat="Integer")
total_camas = int(input("Ingrese el número total de camas en el hospital: ")) #Indicamos en la terminal el número de camas del hospital
total_medicos = int(input("Ingrese el número total de medicos en el hospital: ")) #Indicamos en la terminal el número de médicos del hospital
turno_medicos = (total_medicos*31)/100 #El número de médicos trabajando en urgencias es del 31%)

presupuesto=2900000 #Presupuesto del hospital de urgencias ZENDAL. Habría que encontrar el presupuesto del hospital La Paz
pacientes=500

#Función a optimizar. Se desembolsan 5141€ por cada cama en uso y 2694€ por cada médico trabajando
modelo += camas_utilizadas*5141 + medicos_trabajando*2694

#Restricciones
modelo += medicos_trabajando*2694 + camas_utilizadas*5141 <= presupuesto  #El gasto en camas debe ser menor al presupuesto
modelo += camas_liberadas + camas_utilizadas == total_camas 
modelo += camas_utilizadas == pacientes #Las camas utilizadas es igual al número de pacientes
modelo += medicos_libres + medicos_trabajando == turno_medicos

modelo.solve()

#Imprimimos por pantalla los resultados que nos interesan
print("Tenemos un presupuesto de:", int(presupuesto), "€")
print("\t Encontramos {} camas libres".format(int(camas_liberadas.varValue)))
print("\t Encontramos {} camas en uso por las que se desembolsan {}".format(int(camas_utilizadas.varValue), int(camas_utilizadas.varValue*5141)))
print("\t Necesitamos {} médicos para cubrir las camas en uso. Podemos liberar a {} médicos.".format(int(medicos_trabajando.varValue), int(medicos_libres.varValue)))

if  medicos_trabajando.varValue*2694 + camas_utilizadas.varValue*5141 > presupuesto:
    print("ERROR. Hay", int(pacientes-camas_utilizadas.varValue), "que no pueden ser atendidos de forma correcta por la limitación de presupuesto. Necesitamos:" , int(medicos_trabajando.varValue*2694 + pacientes*5141 - presupuesto), "€ más" )
else:
    print("\t Presupuesto utilizado:", medicos_trabajando.varValue*2694 + camas_utilizadas.varValue*5141, "\n \tPresupuesto sobrante:", presupuesto-(medicos_trabajando.varValue*2694 + camas_utilizadas.varValue*5141))