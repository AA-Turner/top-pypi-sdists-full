# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Tuple, Type

if TYPE_CHECKING:
    from ...world import World

# ======================================== ABSTRACT CLASS ========================================
class System(ABC):
    """Classe abstraite des systèmes"""
    __slots__ = tuple()

    order: ClassVar[int] = 0
    exclusive: ClassVar[bool] = False
    renderable: ClassVar[bool] = False

    requires: ClassVar[Tuple[str, ...]] = tuple()
    conflicts: ClassVar[Tuple[str, ...]] = tuple()

    # ======================================== CONTRACT ========================================
    @abstractmethod
    def __repr__(self): ...

    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def update(self, world: World, dt: float): ...