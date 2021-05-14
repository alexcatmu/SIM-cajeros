from itertools import count
class Person:

    id = count(0)

    def __init__(self):
        self.id = next(self.id)
        self.tempsArribadaCua = 0
        self.cola = None
        print("se ha creado una persona con id " + str(self.id))
