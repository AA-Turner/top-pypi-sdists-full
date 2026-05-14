# ======================================== IMPORTS ========================================
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Self

if TYPE_CHECKING:
    from .._rendering import Window
    from .._managers import ContextManager

# ======================================== ABSTRACT CLASS ========================================
class Manager(ABC):
    """Classe abstraite des managers

    Args:
        context_manager: ``Manager`` gérant le contexte d'initialisation
    """
    __slots__ = ("_ctx", "_window")

    _ID: ClassVar[str] = "default"
    _INSTANCE: ClassVar[Manager] = None

    @classmethod
    def get_instance(cls) -> Self:
        """Renvoie l'instance du gestionnaire"""
        if cls._INSTANCE is None:
            from pyverse2d import _context_manager
            cls._INSTANCE = getattr(_context_manager, cls._ID)
        return cls._INSTANCE

    def __init__(self, context_manager: ContextManager):
        # Manager des gestionnaires
        self._ctx: ContextManager = context_manager

        # Fenêtre
        self._window: Window = None

    # ======================================== BIND WINDOW ========================================
    def bind(self, window: Window) -> None:
        """Lie le gestionnaire à une fenêtre

        Args:
            window: fenêtre à assigner
        """
        self._window = window
        
    # ======================================== LIFE CYCLE ========================================
    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def flush(self) -> None: ...