import numpy as np
from Enumeracions import TYPE_EVENT, SERVER_STATE
from Person import Person
from Server import *


def exponential_distribution(time):
    return np.random.exponential(scale=time)


class Source:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatsCreades = 0
        self.state = 'IDLE'
        self.scheduler = scheduler

    def crearConnexio(self, cues_de_caixer):
        self.cues_de_caixer = cues_de_caixer

    def tractarEsdeveniment(self, event):
        if event.type == TYPE_EVENT['start']:
            self.simulationStart(event)

        if event.type == TYPE_EVENT['next_arrival']:
            self.processNextArrival(event)

    def simulationStart(self, event):
        entitat = self.crearPersona()
        cua_mes_buida = self.cues_de_caixer[0]
        entitat.cua = cua_mes_buida.id
        cua_mes_buida.recullEntitat(event.time, entitat)
        nouEvent = self.properaArribada(0, entitat)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def processNextArrival(self, event):
        #Creem persona si encara no s'ha arribat al nombre de persones màxim
        if self.scheduler.entities_quantity < self.entitatsCreades:
            print("Ja no arribaran més persones")
            return None
        entitat = self.crearPersona()
        #Comparar cues dels caixers i agafar la cua més buida per afegir a la persona a aquesta
        cua_mes_buida = self.cues_de_caixer[0]
        canBreak = False
        for cua in self.cues_de_caixer:
            for caixer in cua.caixers:
                if caixer.state == SERVER_STATE["idle"]:
                    cua_mes_buida = cua
                    canBreak = True
                    break
            if canBreak:
                break
            if (len(cua.entitats) / len(cua.caixers)) < (len(cua_mes_buida.entitats) / len(cua_mes_buida.caixers)):
                cua_mes_buida = cua

        entitat.cua = cua_mes_buida.id
        cua_mes_buida.recullEntitat(event.time, entitat)

        nouEvent = self.properaArribada(event.time, entitat)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def properaArribada(self, time, entitat):
        #Arribada exponencial de persones
        tempsEntreArribades = exponential_distribution(self.scheduler.time_between_arrivals)
        # incrementem estadistics si s'escau
        self.entitatsCreades = self.entitatsCreades + 1
        self.state = 'BUSY'
        #Programació seguent arribada
        return Event(self, TYPE_EVENT["next_arrival"], time + tempsEntreArribades, entitat)

    def crearPersona(self):
        nova_persona = Person()
        return nova_persona
