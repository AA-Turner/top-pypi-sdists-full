# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, Any

# ======================================== ABSTRACT CLASS ========================================
class MathObject(ABC):
    """Classe abstraite des objets mathématiques"""
    __slots__ = tuple()

    def __init__(self):
        ...

    # ======================================== CONVERSIONS ========================================
    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __iter__(self) -> Iterator: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def to_tuple(self) -> tuple: ...

    @abstractmethod
    def to_list(self) -> list: ...
    
    # ======================================== GETTERS ========================================
    @abstractmethod
    def __len__(self) -> int: ...

    # ======================================== COMPARATORS ========================================
    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...

    # ======================================== PUBLIC METHODS ========================================
    @abstractmethod
    def copy(self) -> MathObject: ...