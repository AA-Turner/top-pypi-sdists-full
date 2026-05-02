# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...world import World

# ======================================== ABSTRACT CLASS ========================================
class System(ABC):
    """Classe abstraite des systèmes"""
    __slots__ = tuple()
    order: int = 0
    exclusive: bool = False
    requires: tuple[type, ...] = ()
    conflicts: tuple[type, ...] = ()

    # ======================================== CONTRACT ========================================
    @abstractmethod
    def __repr__(self): ...

    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def update(self, world: World, dt: float): ...