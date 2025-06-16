from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from whiskerrag_types.model.knowledge import Knowledge
from whiskerrag_types.model.multi_modal import Image, Text

T = TypeVar("T", Image, Text)


class BaseLoader(ABC, Generic[T]):
    def __init__(self, knowledge: Knowledge):
        self.knowledge = knowledge

    @abstractmethod
    async def load(self) -> List[T]:
        """
        Load the knowledge into a list of items.
        This method should be implemented by subclasses to define how the knowledge is loaded.
        """
        pass

    @abstractmethod
    async def decompose(self) -> List[Knowledge]:
        """
        Decompose the knowledge into smaller parts.
        This method should be implemented by subclasses to define how the knowledge is decomposed.
        """
        pass

    @abstractmethod
    async def on_load_finished(self) -> None:
        """
        Lifecycle method called when the loading task is finished.
        Subclasses can implement this to perform any cleanup or post-processing.
        """
        pass
