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
        self.seed = None

    def addEntity(self, entity):
        self.entities.append(entity)

    def to_json(self):
        jsonStr = json.dumps(self, default=lambda x: x.__dict__)
        return jsonStr

    def clear(self):
        self.entities = []
        self.seed = None