from abc import ABC, abstractmethod
from typing import Any, List


class IEntityExtractor(ABC):
    @abstractmethod
    def extract(self, entity: Any) -> List[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
