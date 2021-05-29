import sys
import numpy as np
from Scheduler import Scheduler
from Settings import START_SEED, ENTITIES_QUANTITY, TIME_BETWEEN_ARRIVALS, TIME_PROCESSING, QUANTITY_OF_EXPERIMENTS
from Statistics import Statistics
from Analyzer import CalcularResultats

print("Hola, se va a iniciar la simulación con los siguientes parámetros:")
print("Cantidad de entidades del sistema:", ENTITIES_QUANTITY)
print("Tiempo medio entre llegadas:", TIME_BETWEEN_ARRIVALS)
print("Tiempo medio de proceso:", TIME_PROCESSING)
print("Semilla para las distribuciones:", START_SEED)
print("Cantidad de experimentos:", QUANTITY_OF_EXPERIMENTS)


cambiar_parametros = input("Desea cambiar los parámetros de configuración(s/n): ")

if (cambiar_parametros == 's'):
    ENTITIES_QUANTITY = int(input("Cantidad de entidades del sistema: "))
    TIME_BETWEEN_ARRIVALS = int(input("Tiempo medio entre llegadas: "))
    TIME_PROCESSING = int(input("Tiempo medio de proceso: "))
    START_SEED = int(input("Semilla para las distribuciones: "))
    QUANTITY_OF_EXPERIMENTS = int(input("Cantidad de experimentos: "))




seed = START_SEED
np.random.seed(seed)
experiments_finished = []
first_experiment = 1


### LIMPIAR FICHERO STATISTICS ####
statistics_output = open('statistics.json', 'w')
statistics_output.close()

### ABRIR EN MODO APPEND EL FICHERO STATISTICS
statistics_output = open('statistics.json', 'a')
statistics_output.write('[')

for actual_experiment in range(first_experiment, QUANTITY_OF_EXPERIMENTS + 1):
    Statistics().seed = seed
    scheduler = Scheduler()

    scheduler.run(entities_quantity=ENTITIES_QUANTITY, time_between_arrivals=TIME_BETWEEN_ARRIVALS,
                  time_processing=TIME_PROCESSING)

    experiments_finished.append(Statistics().to_json())
    statistics_output.write(Statistics().to_json())
    if actual_experiment < QUANTITY_OF_EXPERIMENTS:
        statistics_output.write(',')
    seed += 1
    Statistics().clear()
    print("##################################################")
    print("##################################################")
    print("##################################################")
    print("##################################################")

statistics_output.write(']')
statistics_output.close()
CalcularResultats()

