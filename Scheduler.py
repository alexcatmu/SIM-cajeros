import os
import sys

from Settings import ENTITIES_QUANTITY, TIME_BETWEEN_ARRIVALS, TIME_PROCESSING, START_SEED, QUANTITY_OF_EXPERIMENTS
from Source import *
from Event import *
from Server import Server
from MyQueue import MyQueue
from Enumeracions import TYPE_EVENT
from Statistics import Statistics


class Scheduler:

    def __init__(self):

        self.currentTime = 0
        self.eventList = []

        self.statistics = Statistics()
        self.source = Source(self)

        self.cua_unica = MyQueue("cua_unica")
        self.caixer_cua_unica1 = Server(self, "caixer_cua_unica1")
        self.caixer_cua_unica2 = Server(self, "caixer_cua_unica2")
        self.caixer_cua_unica3 = Server(self, "caixer_cua_unica3")
        self.cua_unica.crearConnexio([self.caixer_cua_unica1, self.caixer_cua_unica2, self.caixer_cua_unica3])
        self.caixer_cua_unica1.crearConnexio(self.cua_unica)
        self.caixer_cua_unica2.crearConnexio(self.cua_unica)
        self.caixer_cua_unica3.crearConnexio(self.cua_unica)

        self.cua_caixer4 = MyQueue("cua_caixer4")
        self.caixer4 = Server(self, "caixer4")
        self.cua_caixer4.crearConnexio([self.caixer4])
        self.caixer4.crearConnexio(self.cua_caixer4)

        self.cua_caixer5 = MyQueue("cua_caixer5")
        self.caixer5 = Server(self, "caixer5")
        self.cua_caixer5.crearConnexio([self.caixer5])
        self.caixer5.crearConnexio(self.cua_caixer5)

        self.cua_caixer6 = MyQueue("cua_caixer6")
        self.caixer6 = Server(self, "caixer6")
        self.cua_caixer6.crearConnexio([self.caixer6])
        self.caixer6.crearConnexio(self.cua_caixer6)

        self.source.crearConnexio([self.cua_unica, self.cua_caixer4, self.cua_caixer5, self.cua_caixer6])

        self.simulationStart = Event(self, TYPE_EVENT['start'], self.currentTime, None)
        self.eventList.append(self.simulationStart)

    def run(self, entities_quantity, time_between_arrivals, time_processing):
        # configurar el model per consola, arxiu de text...
        self.configurarModel(entities_quantity, time_between_arrivals, time_processing)

        # rellotge de simulacio a 0
        self.currentTime = 0
        # bucle de simulació (condició fi simulació llista buida)
        while len(self.eventList) > 0:
            # recuperem event simulacio
            event = self.getEvent()
            # actualitzem el rellotge de simulacio
            self.currentTime = event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            print("------------------------------------------------")
            print("A l'instant", event.time, ":")
            event.object.tractarEsdeveniment(event)
            print("------------------------------------------------\n")

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        self.eventList.append(event)
        self.eventList.sort(key=lambda x: x.time)
        return None

    def tractarEsdeveniment(self, event):
        if (event.type == TYPE_EVENT['start']):
            print("S'està iniciant la simulació")
            self.source.simulationStart(event)

    def configurarModel(self, entities_quantity, time_between_arrivals, time_processing):
        self.entities_quantity = entities_quantity
        self.time_between_arrivals = time_between_arrivals
        self.time_processing = time_processing
        print("Configurant el model...")

    def getEvent(self):
        event = self.eventList[0]  # [1,2,3,4,5]
        self.eventList = self.eventList[1:]  # [2,3,4,5]
        return event


if __name__ == "__main__":
    print(sys.argv)
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
        if (actual_experiment < QUANTITY_OF_EXPERIMENTS):
            statistics_output.write(',')
        seed += 1
        Statistics().clear()
    statistics_output.seek(statistics_output.tell() - 1, os.SEEK_SET)
    statistics_output.write(']')
    statistics_output.close()
