# flake8: noqa: I003

from abc import abstractmethod, ABC
from fabric.functions.fabric_item import FabricItem


class BaseFabricItemProvider(ABC):
    
    @abstractmethod
    def create(self, item: FabricItem, **kwargs) -> None:
        """ Must be implemented by subclasses """
        pass