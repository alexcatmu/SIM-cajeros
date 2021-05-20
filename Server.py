import numpy as np
from Enumeracions import SERVER_STATE, TYPE_EVENT, QUEUE_STATE
from Event import *


def normal(time_processing):
    return np.random.normal(time_processing,time_processing/3,1)[0]


class Server:

    def __init__(self, scheduler, id):
        # inicialitzar element de simulació
        self.id = id
        self.entitatsTractades = 0
        self.state = SERVER_STATE['idle']
        self.scheduler = scheduler
        self.entitatActiva = None

    def crearConnexio(self, queue):
        self.queue = queue

    def recullEntitat(self, time, entitat):
        print("Ha arribat al", self.id ,"la persona", entitat.id)
        entitat.tempsIniciServei = time
        nouEvent = self.programarFinalServei(time, entitat)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def tractarEsdeveniment(self, event):
        if (event.type == TYPE_EVENT['start']):
            self.simulationStart(event)

        if (event.type == TYPE_EVENT['end_service']):
            self.processarFiServei(event)

    def programarFinalServei(self, time, entitat):
        # que triguem a fer un servei (aleatorietat)
        tempsServei = normal(self.scheduler.time_processing)
        entitat.tempsSortida = time + tempsServei
        # incrementem estadistics si s'escau
        self.entitatsTractades = self.entitatsTractades + 1
        self.state = SERVER_STATE["busy"]
        # programació final servei
        return Event(self, TYPE_EVENT["end_service"], time + tempsServei, entitat)

    def processarFiServei(self, event):
        # Registrar estadístics
        print("La persona " + str(event.entity.id) + " ha marxat del " + self.id)
        self.entitatsTractades = self.entitatsTractades + 1
        self.state = SERVER_STATE["idle"]
        self.queue.enviarPersonaAlCaixer(event.time)












