class Statistics:
    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    def analyzeEvents(self):
        print("Analitzant tots els esdeveniments...\n")
        print("RESULTATS:")
        print(len(self.events))


