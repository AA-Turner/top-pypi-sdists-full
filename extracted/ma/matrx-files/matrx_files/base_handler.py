
from abc import ABC, abstractmethod
from typing import Any


class BaseHandler(ABC):
    @abstractmethod
    def read(self, path: Any) -> Any:
        pass

    @abstractmethod
    def write(self, path: Any, content: Any) -> bool:
        pass

    @abstractmethod
    def append(self, path: Any, content: Any) -> bool:
        pass

    @abstractmethod
    def delete(self, path: Any) -> bool:
        pass
