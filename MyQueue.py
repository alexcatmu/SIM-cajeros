from queue import Queue
from Enumeracions import QUEUE_STATE, SERVER_STATE


class MyQueue(Queue):
    def __init__(self, id):
        Queue.__init__(self)
        self.id = id
        self.caixers = None
        self.entitats = []
        self.state = QUEUE_STATE["empty"]

    def crearConnexio(self, cajero):
        self.caixers = cajero

    def recullEntitat(self, time, entitat):
        print("Ha arribat a la", self.id , "la persona", entitat.id)
        self.entitats.append(entitat)
        #Temps d'arribada a la cua per poder mirar si ha de canviar de cua
        entitat.tempsArribadaCua = time
        if (self.state == QUEUE_STATE["empty"]):
            self.state = QUEUE_STATE["occupied"]
        self.enviarPersonaAlCaixer(time)

    def enviarPersonaAlCaixer(self, time):
        for caixer in self.caixers:
            if caixer.state == SERVER_STATE["idle"] and self.state == QUEUE_STATE["occupied"]:
                persona = self.entitats[0]
                self.entitats = self.entitats[1:]
                if len(self.entitats) == 0:
                    self.state = QUEUE_STATE["empty"]
                caixer.recullEntitat(time, persona)

