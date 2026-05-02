# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..abc import Manager

from ._context import ContextManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..abc import Widget

# ======================================== GESTIONNAIRE ========================================
class UiManager(Manager):
    """Gestionnaire de l'ui"""
    __slots__ = (
        "_ctx",
        "_hovered", "_focused",
    )

    _ID: str = "ui"

    def __init__(self, context_manager: ContextManager):
        # Contexte de managers
        self._ctx: ContextManager = context_manager

        # Widgets dominants
        self._hovered: Widget = None        # Widget survolé
        self._focused: Widget = None        # Widget concentré

    # ======================================== STATES ========================================
    @property
    def hovered(self) -> Widget | None:
        """Widget survolé"""
        return self._hovered
    
    @property
    def focused(self) -> Widget | None:
        """Widget concentré"""
        return self._focused
    
    def unhover(self) -> None:
        """Enlève le survol"""
        self._hovered = None
    
    def unfocus(self) -> None:
        """Enlève la concentration"""
        self._focused = None

    # ======================================== REQUESTS ========================================
    def ask_hover(self, widget: Widget) -> None:
        """Demande à survoler un widget
        
        Args:
            widget: ``Widget`` demandeur
        """
        if self._hovered is not None:
            return False
        self._hovered = widget
        return True

    def ask_focus(self, widget: Widget) -> None:
        """Demande à concentrer un widget
        
        Args:
            widget: ``Widget`` demandeur
        """
        if self._focused is not None:
            return False
        self._focused = widget
        return True

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        pass

    def flush(self) -> None:
        """Nettoyage"""
        self._hovered = None
        self._focused = None

# ======================================== EXPORTS ========================================
__all__ = [
    "UiManager",
]