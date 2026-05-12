# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import profile_section
from ..abc import Manager

from ._context import ContextManager

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from ..abc import Widget

# ======================================== GESTIONNAIRE ========================================
class UiManager(Manager):
    """Gestionnaire de l'ui

    Args:
        context_manager: ``Manager`` gérant le contexte d'initialisation
    """
    __slots__ = (
        "_ctx",
        "_hovered", "_focused",
    )

    _ID: ClassVar[str] = "ui"

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
    @profile_section("manager.ui.update")
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        pass

    @profile_section("manager.ui.flush")
    def flush(self) -> None:
        """Nettoyage"""
        self._hovered = None
        self._focused = None

# ======================================== EXPORTS ========================================
__all__ = [
    "UiManager",
]