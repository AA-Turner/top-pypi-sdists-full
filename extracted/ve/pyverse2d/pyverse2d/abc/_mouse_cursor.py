# ======================================== IMPORTS ========================================
from __future__ import annotations

from pyglet.window import MouseCursor

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._rendering import Window

# ======================================== ABSTRACT CLASS ========================================
class MouseCursor(ABC):
    """Curseur de souris abstrait"""

    @abstractmethod
    def to_pyglet(self, window: Window) -> MouseCursor:
        """Convertit en curseur pyglet"""
        ...