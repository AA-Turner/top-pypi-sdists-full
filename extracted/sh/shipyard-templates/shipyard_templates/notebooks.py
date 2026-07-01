from abc import ABC, abstractmethod


class Notebooks(ABC):
    @abstractmethod
    def connect(self):
        pass
