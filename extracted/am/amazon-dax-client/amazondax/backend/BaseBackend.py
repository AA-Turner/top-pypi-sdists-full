from abc import ABC, abstractmethod


class BaseBackend(ABC):
    '''Abstract base class for cluster backend implementations.'''

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def update(self, new_service_endpoint):
        pass

    @abstractmethod
    def is_closed(self):
        pass

    @property
    @abstractmethod
    def addrport(self):
        pass

    @property
    @abstractmethod
    def role(self):
        pass

    @property
    @abstractmethod
    def leader(self):
        pass
