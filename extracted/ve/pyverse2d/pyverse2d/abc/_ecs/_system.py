# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Tuple

if TYPE_CHECKING:
    from ...world import World

# ======================================== ABSTRACT CLASS ========================================
class System(ABC):
    """Classe abstraite des systèmes"""
    __slots__ = tuple()

    _ORDER: ClassVar[int] = 0
    
    _IS_EXCLUSIVE: ClassVar[bool] = False
    _IS_RENDERABLE: ClassVar[bool] = False

    _REQUIRES: ClassVar[Tuple[str, ...]] = tuple()
    _CONFLICTS: ClassVar[Tuple[str, ...]] = tuple()

    # ======================================== CONTRACT ========================================
    @abstractmethod
    def __repr__(self): ...

    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def update(self, world: World, dt: float): ...

# ======================================== EXPORTS ========================================
__all__ = [
    "System",
]