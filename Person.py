from itertools import count
class Person:

    id = count(0)

    def __init__(self):
        self.id = next(self.id)
        self.tempsArribadaCua = 0
        self.cua = None
        print("S'ha creat la persona amb id " + str(self.id))
