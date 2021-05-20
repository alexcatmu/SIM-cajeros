from itertools import count
from Statistics import Statistics
class Person:

    id = count(0)

    def __init__(self):
        self.id = next(self.id)
        self.tempsArribada = 0
        self.tempsArribadaCua = 0
        self.tempsIniciServei = 0
        self.tempsSortida = 0
        self.cua = None
        Statistics().addEntity(self)
        print("S'ha creat una persona amb id " + str(self.id))
