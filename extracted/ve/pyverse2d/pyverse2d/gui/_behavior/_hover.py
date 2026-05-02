# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import CallbackList
from ...abc import Behavior
from ...math import Point

from pyverse2d import mouse, ui

# ======================================== BEHAVIOR ========================================
class HoverBehavior(Behavior):
    """Behavior gérant le survol"""
    __slots__ = (
        "_hovered",
        "_on_enter", "_on_leave",
        "_when_hovered", "_when_unhovered",
    )
    _ID: str = "hover"
    _PRIORITY: int = 1

    def __init__(self):
        # Initialisation du comportement
        super().__init__()

        # Etat
        self._hovered: bool = False

        # Hooks
        self._on_enter: CallbackList = CallbackList()
        self._on_leave: CallbackList = CallbackList()
        self._when_hovered: CallbackList = CallbackList()
        self._when_unhovered: CallbackList = CallbackList()

        # Tweens
        self._on_enter(self._play_tweens)
        self._on_leave(self._reverse_tweens)
        
    # ======================================== PROPERTIES ========================================
    @property
    def on_enter(self) -> CallbackList:
        """Fonctions appelées à l'entrée"""
        return self._on_enter
    
    @property
    def on_leave(self) -> CallbackList:
        """Fonctions appelées à la sortie"""
        return self._on_leave

    @property
    def when_hovered(self) -> CallbackList:
        """Fonctions appelées durant le survol"""
        return self._when_hovered
    
    @property
    def when_unhovered(self) -> CallbackList:
        """Fonctions appelées durant le non-survol"""
        return self._when_unhovered

    # ======================================== PREDICATES ========================================
    def is_hovered(self) -> bool:
        """Indique si le widget est survolé"""
        return self._hovered

    # ======================================== HOOKS ========================================
    def _on_attach(self) -> None:
        """Hook d'attachement"""
        pass

    def _on_detach(self) -> None:
        """Hook de détachement"""
        if self._hovered:
            ui.unhover()

    def _on_enable(self) -> None:
        """Hook d'activation"""
        pass

    def _on_disable(self) -> None:
        """Hook de désactivation"""
        if self._hovered:
            self._on_leave.trigger()
            self._hovered = False
            ui.unhover()

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation"""
        # Détection du survol
        if ui.hovered is None and self._collides(mouse.get_world_position()):
            hovered = ui.ask_hover(self._owner)
        else:
            hovered = False

        # Hooks de changement d'état
        if hovered:
            if not self._hovered:
                self.on_enter.trigger()
            self.when_hovered.trigger()
        else:
            if self._hovered:
                self.on_leave.trigger()
            self.when_unhovered.trigger()
        self._hovered = hovered

    # ======================================== HELPERS ========================================
    def _collides(self, point: Point) -> bool:
        """Vérifie si un point est dans le widget"""
        return self._owner.collidespoint(point)