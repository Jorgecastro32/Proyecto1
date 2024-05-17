import matplotlib.pyplot as plt
import numpy as np

def crear_diagrama_conjunto():
    # Definir los datos
    camas_iniciales = 892
    medicos_iniciales = 179
    tiempo_inicial = 90

    camas_nuevas = 528
    medicos_nuevos = 105
    tiempo_nuevo = 90-5.573430386070818

    # Crear las etiquetas y los valores
    labels = ['Camas', 'Médicos']
    valores_iniciales = [camas_iniciales, medicos_iniciales]
    valores_nuevos = [camas_nuevas, medicos_nuevos]
    valores_totales = [camas_iniciales + camas_nuevas, medicos_iniciales + medicos_nuevos]

    # Definir la posición de las barras en el eje x
    x = np.arange(len(labels))

    # Ancho de las barras
    ancho = 0.5

    # Crear el gráfico de barras apiladas
    fig, ax = plt.subplots(figsize=(12, 8))
    barras1 = ax.bar(x, valores_iniciales, ancho, label='Iniciales', color='blue')
    barras2 = ax.bar(x, valores_nuevos, ancho, bottom=valores_iniciales, label='Nuevas', color='green')

    # Ajustar los márgenes y separaciones
    plt.subplots_adjust(top=0.85, bottom=0.15, left=0.1, right=0.9, hspace=0.5, wspace=0.5)

    # Añadir el tiempo como texto
    ax.text(-0.1, max(valores_totales) + 200, f'Tiempo inicial: {tiempo_inicial} min', fontsize=12)
    ax.text(0.9, max(valores_totales) + 200, f'Tiempo optimizado: {tiempo_nuevo:.2f} min', fontsize=12)

    # Añadir título y etiquetas
    ax.set_title('Camas y Médicos Hospital \nRamón y Cajal antes y después de la Optimización', fontsize=16)
    ax.set_xlabel('Recursos', fontsize=14)
    ax.set_ylabel('Cantidad', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Mostrar el gráfico
    plt.show()

# Llamar a la función para crear el gráfico conjunto
crear_diagrama_conjunto()
