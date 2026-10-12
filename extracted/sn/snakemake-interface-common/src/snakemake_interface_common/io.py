from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Dict, Optional


class AccessPattern(StrEnum):
    RANDOM = "random"
    SEQUENTIAL = "sequential"
    MULTI = "multi"


class AnnotatedStringInterface(ABC):
    """Interface for annotated strings/callables as they are used for input/output in
    Snakemake rules.
    """

    @property
    @abstractmethod
    def flags(self) -> Dict[str, Any]: ...

    @abstractmethod
    def is_callable(self) -> bool: ...

    def is_flagged(self, flag: str) -> bool:
        return flag in self.flags and bool(self.flags[flag])

    @abstractmethod
    def access_pattern(self) -> Optional[AccessPattern]: ...
