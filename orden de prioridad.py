import heapq

class Paciente:
    def __init__(self, nombre, prioridad):
        self.nombre = nombre
        self.prioridad = prioridad

def obtener_datos_pacientes():
    try:
        num_pacientes = int(input("Ingrese el número de pacientes: "))
        pacientes = []

        for i in range(1, num_pacientes + 1):
            nombre = input(f"Ingrese el nombre del paciente {i}: ")
            prioridad= int(input(f"Ingrese la prioridad del paciente {i} (mayor número indica menor prioridad): "))
            pacientes.append(Paciente(nombre, prioridad))

        return pacientes
    except ValueError:
        print("Error: Ingrese un valor válido acorde a la información solicitada.")
        return obtener_datos_pacientes()

def optimizar_listas_espera(pacientes):
    cola_prioridad = []

    for paciente in pacientes:
        heapq.heappush(cola_prioridad, (paciente.prioridad, paciente.nombre))

    lista_optimizada = []

    while cola_prioridad:
        _, paciente_actual = heapq.heappop(cola_prioridad)
        lista_optimizada.append(paciente_actual)

    return lista_optimizada

# Obtener datos de los pacientes
pacientes = obtener_datos_pacientes()

# Optimizar la lista de espera
lista_optimizada = optimizar_listas_espera(pacientes)

# Mostrar la lista de espera optimizada
print("\nLista de espera optimizada:")
print(lista_optimizada)