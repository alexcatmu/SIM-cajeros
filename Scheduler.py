import sys

from Server import *
from Source import *
from Event import *
from Server import Server
from MyQueue import MyQueue
from Enumeracions import TYPE_EVENT
from Statistics import Statistics


class Scheduler:
    currentTime = 0
    eventList = []

    def __init__(self):
        # creador de personas que entran al supermercado
        self.statistics = Statistics()
        self.source = Source(self)

        self.cola_unica = MyQueue("cola_unica")
        self.cajero_cola_unica1 = Server(self, "cajero_cola_unica1")
        self.cajero_cola_unica2 = Server(self, "cajero_cola_unica2")
        self.cajero_cola_unica3 = Server(self, "cajero_cola_unica3")
        self.cola_unica.crearConnexio([self.cajero_cola_unica1, self.cajero_cola_unica2, self.cajero_cola_unica3])
        self.cajero_cola_unica1.crearConnexio(self.cola_unica)
        self.cajero_cola_unica2.crearConnexio(self.cola_unica)
        self.cajero_cola_unica3.crearConnexio(self.cola_unica)

        self.cola_cajero4 = MyQueue("cola_cajero4")
        self.cajero4 = Server(self, "cajero4")
        self.cola_cajero4.crearConnexio([self.cajero4])
        self.cajero4.crearConnexio(self.cola_cajero4)

        self.cola_cajero5 = MyQueue("cola_cajero5")
        self.cajero5 = Server(self, "cajero5")
        self.cola_cajero5.crearConnexio([self.cajero5])
        self.cajero5.crearConnexio(self.cola_cajero5)

        self.cola_cajero6 = MyQueue("cola_cajero6")
        self.cajero6 = Server(self, "cajero6")
        self.cola_cajero6.crearConnexio([self.cajero6])
        self.cajero6.crearConnexio(self.cola_cajero6)

        self.source.crearConnexio([self.cola_unica, self.cola_cajero4, self.cola_cajero5, self.cola_cajero6])

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
            print("En el instante", event.time, ":")
            event.object.tractarEsdeveniment(event)
            print("------------------------------------------------\n")

        # recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        self.eventList.append(event)
        self.eventList.sort(key=lambda x: x.time)
        return None

    def tractarEsdeveniment(self, event):
        if (event.type == TYPE_EVENT['start']):
            print("esta iniciando la simulacion")
            self.source.simulationStart(event)

    def recollirEstadistics(self):
        self.statistics.analyzeEvents()

    def configurarModel(self, entities_quantity, time_between_arrivals, time_processing):
        self.entities_quantity = entities_quantity
        self.time_between_arrivals = time_between_arrivals
        self.time_processing = time_processing
        print("estoy configurando el modelo")

    def getEvent(self):
        event = self.eventList[0]  # [1,2,3,4,5]
        self.statistics.addEvent(event)
        self.eventList = self.eventList[1:]  # [2,3,4,5]
        return event


if __name__ == "__main__":
    print(sys.argv)
    scheduler = Scheduler()
    scheduler.run(entities_quantity=25, time_between_arrivals=2, time_processing=10)
