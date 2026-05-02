# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

# ======================================== ABSTRACT CLASS ========================================
class Component(ABC):
    """Classe abstraite des composants"""
    __slots__ = ()
    requires: tuple[type, ...] = ()
    conflicts: tuple[type, ...] = ()

    # ======================================== CONTRACT ========================================
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def __repr__(self) -> str: ...

    def __iter__(self) -> Iterator:
        """Renvoie le composant dans un itérateur"""
        return iter(self.get_attributes())
    
    def __hash__(self) -> int:
        """Renvoie l'entier hashé du composant"""
        return hash(self.get_attributes())

    @abstractmethod
    def get_attributes(self) -> tuple: ...

    @abstractmethod
    def copy(self) -> Component: ...

    # ======================================== COMPARATORS ========================================
    def __eq__(self, other: object) -> bool:
        """Vérifie la correspondance de deux composants"""
        if isinstance(other, Component):
            return self.get_attributes() == other.get_attributes()
        return NotImplemented