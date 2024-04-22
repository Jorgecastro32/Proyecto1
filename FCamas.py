from pulp import *
#Variables
modelo = LpProblem("Minimizar tiempo", sense= LpMaximize)
medicos_operando= LpVariable("Médicos operando", lowBound=0, upBound=10, cat="Integer")
medicos_libres=LpVariable("Médicos libres", lowBound=0, upBound=10, cat="Integer")

#Función a optimizar. 2 horas por operación y una hora de descanso
modelo += medicos_operando*2+ medicos_libres

#Restricciones
modelo += medicos_libres + medicos_operando<=10

modelo.solve()

print("Encontramos {} médicos libres".format(medicos_libres.varValue))
print("Encontramos {} médicos operando".format(medicos_operando.varValue))