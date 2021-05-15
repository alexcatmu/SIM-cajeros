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

        # recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        self.eventList.append(event)
        self.eventList.sort(key=lambda x: x.time)
        return None

    def tractarEsdeveniment(self, event):
        if (event.type == TYPE_EVENT['start']):
            print("S'està iniciant la simulació")
            self.source.simulationStart(event)

    def recollirEstadistics(self):
        print("Recollint estadístics...")
        self.statistics.analyzeEvents()

    def configurarModel(self, entities_quantity, time_between_arrivals, time_processing):
        self.entities_quantity = entities_quantity
        self.time_between_arrivals = time_between_arrivals
        self.time_processing = time_processing
        print("Configurant el model...")

    def getEvent(self):
        event = self.eventList[0]  # [1,2,3,4,5]
        self.statistics.addEvent(event)
        self.eventList = self.eventList[1:]  # [2,3,4,5]
        return event


if __name__ == "__main__":
    print(sys.argv)
    scheduler = Scheduler()
    scheduler.run(entities_quantity=25, time_between_arrivals=2, time_processing=10)
