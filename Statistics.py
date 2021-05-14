class Statistics:
    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    def analyzeEvents(self):
        print("analizando eventos")
        print(len(self.events))


