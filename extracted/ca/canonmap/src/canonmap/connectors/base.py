# src/canonmap/connectors/base.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

class BaseConnector(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def run_query(self, query: str, params: Optional[Union[List, Dict]] = None) -> List[Dict]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        pass