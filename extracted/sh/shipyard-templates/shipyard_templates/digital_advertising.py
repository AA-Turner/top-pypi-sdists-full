from abc import ABC, abstractmethod


class DigitalAdvertising(ABC):
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def read(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass
