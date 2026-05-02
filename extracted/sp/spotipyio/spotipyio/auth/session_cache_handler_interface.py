from abc import ABC, abstractmethod
from typing import Dict, Optional


class ISessionCacheHandler(ABC):
    @abstractmethod
    def get(self) -> Optional[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def set(self, response: Dict[str, str]) -> None:
        raise NotImplementedError
