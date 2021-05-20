import json
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Statistics(metaclass=SingletonMeta):
    def __init__(self):
        self.entities = []
        #self.time_in_the_queue = []
        #self.entity_life = []
        #self.queue_capacity = []
        #self.time_of_service = []

    def addEntity(self, entity):
        self.entities.append(entity)

    def analyseStatistics(self):
        pass

    def export(self):
        print("HOLA que talrsgsdgsdgsg")
        json.dumps(self.__dict__)
