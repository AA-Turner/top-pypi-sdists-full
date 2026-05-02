# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import CallbackList
from ..._managers._inputs import Listener
from ...abc import Behavior
from ...math import Point

from pyverse2d import mouse, inputs

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .._selection_group import SelectionGroup

# ======================================== BEHAVIOR ========================================
class SelectBehavior(Behavior):
    """Behavior gérant la sélection
    
    Ce ``Behavior`` s'associe automatiquement au ``HoverBehavior`` si le ``Widget`` en possède un.
    """
    __slots__ = (
        "_selection_group", "_selected",
        "_on_select", "_on_deselect",
        "_when_selected", "_when_deselected",
        "_listener",
    )
    _ID: str = "select"
    _PRIORITY: int = 2

    def __init__(self, selection_group: SelectionGroup = None):
        # Initialisation du comportement
        super().__init__()

        # Selection
        self._selection_group: SelectionGroup = selection_group
        self._selected: bool = False

        # Hooks
        self._on_select: CallbackList = CallbackList()
        self._on_deselect: CallbackList = CallbackList()
        self._when_selected: CallbackList = CallbackList()
        self._when_deselected: CallbackList = CallbackList()

        # Listeners
        self._listener: Listener = None

        # Tweens
        self._on_select(self._play_tweens)
        self._on_deselect(self._reverse_tweens)

    # ======================================== PROPERTIES ========================================
    @property
    def selection_group(self) -> SelectionGroup:
        """Groupe de sélection"""
        return self._selection_group

    @property
    def on_select(self) -> CallbackList:
        """Fonctions appelées à la sélection"""
        return self._on_select

    @property
    def on_deselect(self) -> CallbackList:
        """Fonctions appelées à la désélection"""
        return self._on_deselect

    @property
    def when_selected(self) -> CallbackList:
        """Fonctions appelées durant la sélection"""
        return self._when_selected

    @property
    def when_deselected(self) -> CallbackList:
        """Fonctions appelées durant la désélection"""
        return self._when_deselected

    # ======================================== PREDICATES ========================================
    def is_selected(self) -> bool:
        """Indique si le widget est sélectionné"""
        return self._selected

    # ======================================== HOOKS ========================================
    def _on_attach(self) -> None:
        """Hook d'attachement"""
        self._register()
        self._listener: Listener = inputs.add_listener(
            key = mouse.B_LEFT,
            callback = self._handle_click,
            condition = self._is_hovered,
        )

    def _on_detach(self) -> None:
        """Hook de détachement"""
        self._listener.invalidate()
        if self._selection_group is None:
            if self._selected: self.deselect()
        else: 
            self._selection_group.remove(self._owner)

    def _on_enable(self) -> None:
        """Hook d'activation"""
        self._listener.enable()

    def _on_disable(self) -> None:
        """Hook de désactivation"""
        self._listener.disable()
        if self._selected:
            if self._selection_group is None: self.deselect()
            else: self._selection_group.deselect(self._owner)

    # ======================================== STATE ========================================
    def _handle_click(self) -> None:
        """Gère les clics"""
        if self._selection_group is None:
            if self._selected: self.deselect()
            else: self.select()
        else:
            self._selection_group.click(self._owner)

    def select(self) -> None:
        """Sélectionne le widget"""
        if self._selected:
            return
        self._selected = True
        self._on_select.trigger()

    def deselect(self) -> None:
        """Désélectionne le widget"""
        if not self._selected:
            return
        self._selected = False
        self._on_deselect.trigger()

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation"""
        if self._selected:
            self.when_selected.trigger()
        else:
            self.when_deselected.trigger()

    # ======================================== INTERNALS ========================================
    def _register(self) ->  bool:
        """Enregistrement dans la sélection"""
        if self._selection_group is None:
            return
        self._selection_group.add(self._owner)

    def _is_hovered(self) -> bool:
        """Vérifie si le widget est survolé"""
        if self._owner.hover is None:
            return self._collides(mouse.get_world_position())
        return self._owner.hover.is_hovered()

    def _collides(self, point: Point) -> bool:
        """Vérifie si un point est dans le widget"""
        return self._owner.collidespoint(point)