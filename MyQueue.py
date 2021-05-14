from queue import Queue
from Enumeracions import QUEUE_STATE, SERVER_STATE


class MyQueue(Queue):
    def __init__(self, id):
        Queue.__init__(self)
        self.id = id
        self.cajeros = None
        self.entities = []
        self.state = QUEUE_STATE["empty"]

    def crearConnexio(self, cajero):
        self.cajeros = cajero

    def recullEntitat(self, time, entitat):
        print("Ha llegado a la", self.id , "la persona", entitat.id)
        self.entities.append(entitat)
        #Temps d'arribada a la cua per poder mirar si ha de canviar de cua
        entitat.tempsArribadaCua = time
        if (self.state == QUEUE_STATE["empty"]):
            self.state = QUEUE_STATE["occupied"]
        self.enviarPersonaAlCaixer(time)

    def enviarPersonaAlCaixer(self, time):
        for cajero in self.cajeros:
            if cajero.state == SERVER_STATE["idle"] and self.state == QUEUE_STATE["occupied"]:
                persona = self.entities[0]
                self.entities = self.entities[1:]
                if len(self.entities) == 0:
                    self.state = QUEUE_STATE["empty"]
                cajero.recullEntitat(time, persona)

