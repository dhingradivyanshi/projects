from abc import ABC, ABCMeta, abstractmethod

class SingletonMeta(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__()
        return cls._instances[cls]

class DataBase(metaclass=SingletonMeta):
    
    def __init__(self):
        self._db = None

    @abstractmethod
    def _connect(self, *args, **kwargs):
        pass

class MongoDB(DataBase):
    def __init__(self):
        super().__init__()
        self._db = self._connect()
    
    def _connect(self, *args, **kwargs):
        x = {
            "success": True
        }
        return x
x = MongoDB()