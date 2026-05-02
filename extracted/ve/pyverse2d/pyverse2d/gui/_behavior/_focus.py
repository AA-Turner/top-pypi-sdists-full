# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, CallbackList
from ..._managers import InputsManager
from ..._managers._inputs import Listener
from ...abc import Behavior
from ...math import Point

from pyverse2d import key, mouse, inputs

# ======================================== BEHAVIOR ========================================
class FocusBehavior(Behavior):
    """Behavior gérant la concentration

    Ce ``Behavior`` s'associe automatiquement au ``HoverBehavior`` si le ``Widget`` en possède un.

    Args:
        once: annule la concentration après la première action
        unfocus_on_outside_click: annule la concentration lors du clique en dehors du widget
    """
    __slots__ = (
        "_focused", "_once", "_unfocus_on_outside_click", "_unfocus_keys", "_ghost_keys",
        "_on_focus", "_on_unfocus", "_on_keydown", "_on_keyup",
        "_click_listener", "_outside_listeners", "_key_listener",
    )
    _ID: str = "focus"
    _PRIORITY: int = 3

    def __init__(
            self,
            once: bool = False,
            unfocus_on_outside_click: bool = True 
        ):
        # Initialisation du comportement
        super().__init__()

        # Etat
        self._focused: bool = False

        # Paramètres
        self._once: bool = expect(once, bool)
        self._unfocus_on_outside_click: bool = expect(unfocus_on_outside_click, bool)
        self._unfocus_keys: set[InputsManager.Input] = {key.K_ESCAPE}
        self._ghost_keys: set[InputsManager.Input] = set()

        # Hooks
        self._on_focus: CallbackList = CallbackList()
        self._on_unfocus: CallbackList = CallbackList()
        self._on_keydown: CallbackList = CallbackList()
        self._on_keyup: CallbackList = CallbackList()

        # Listeners
        self._click_listener: Listener = None
        self._outside_listeners: set[Listener] = set()
        self._key_listener: Listener = None

        # Tweens
        self._on_focus(self._play_tweens)
        self._on_unfocus(self._reverse_tweens)

    # ======================================== PROPERTIES ========================================
    @property
    def once(self) -> bool:
        """Fin de concentration dés la première action"""
        return self._once
    
    @once.setter
    def once(self, value: bool) -> None:
        self._once = expect(value, bool)

    @property
    def unfocus_on_outside_click(self) -> bool:
        """Fin de concentration lors du clique en dehors du ``Widget``"""
        return self._unfocus_on_outside_click
    
    @unfocus_on_outside_click.setter
    def unfocus_on_outside_click(self, value: bool):
        if self._unfocus_on_outside_click != value:
            self._unfocus_on_outside_click = expect(value, bool)
            if self._owner is not None:
                self._apply_outside_listeners()

    @property
    def on_focus(self) -> CallbackList:
        """Fonctions appelées à la prise de concentration"""
        return self._on_focus

    @property
    def on_unfocus(self) -> CallbackList:
        """Fonctions appelées à la perte de concentration"""
        return self._on_unfocus

    @property
    def on_keydown(self) -> CallbackList:
        """Fonctions appelées à l'appui d'une touche"""
        return self._on_keydown

    @property
    def on_keyup(self) -> CallbackList:
        """Fonctions appelées au relâchement d'une touche"""
        return self._on_keyup

    # ======================================== PREDICATES ========================================
    def is_focused(self) -> bool:
        """Indique si le widget est concentré"""
        return self._focused

    # ======================================== UNFOCUS KEYS ========================================
    def add_unfocus_key(self, k: InputsManager.Input) -> None:
        """Ajoute une clé de fin de concentration"""
        self._unfocus_keys.add(k)
    
    def remove_unfocus_key(self, k: InputsManager.Input) -> None:
        """Retire une clé de fin de concentration"""
        self._unfocus_keys.discard(k)

    def clear_unfocus_keys(self) -> None:
        """Retire l'ensemble des clés de fin de concentration"""
        self._unfocus_keys.clear()

    # ======================================== GHOST KEYS ========================================
    def add_ghost_key(self, k: InputsManager.Input) -> None:
        """Ajoute une touche fantôme (ne déclenche pas once)"""
        self._ghost_keys.add(k)

    def remove_ghost_key(self, k: InputsManager.Input) -> None:
        """Retire une touche fantôme"""
        self._ghost_keys.discard(k)

    def clear_ghost_keys(self) -> None:
        """Retire toutes les touches fantômes"""
        self._ghost_keys.clear()

    # ======================================== STATE ========================================
    def focus(self) -> None:
        """Concentre le widget"""
        if self._focused:
            return
        self._focused = True
        self._on_focus.trigger()

    def unfocus(self) -> None:
        """Retire la concentration du widget"""
        if not self._focused:
            return
        self._focused = False
        self._on_unfocus.trigger()

    # ======================================== HOOKS ========================================
    def _on_attach(self) -> None:
        """Hook d'attachement"""
        self._click_listener = inputs.add_listener(
            key = mouse.B_LEFT,
            callback = self._handle_click,
            condition = self._is_hovered,
        )
        self._key_listener = inputs.when_any(
            callback = self._handle_keydown,
            condition = lambda: self._focused,
            give_key = True,
        )
        self._apply_outside_listeners()

    def _on_detach(self) -> None:
        """Hook de détachement"""
        self._click_listener.invalidate()
        self._key_listener.invalidate()
        self._clear_outside_listeners()
        if self._focused:
            self.unfocus()

    def _on_enable(self) -> None:
        """Hook d'activation"""
        self._click_listener.enable()
        self._key_listener.enable()
        for listener in self._outside_listeners:
            listener.enable()

    def _on_disable(self) -> None:
        """Hook de désactivation"""
        self._click_listener.disable()
        self._key_listener.disable()
        for listener in self._outside_listeners:
            listener.disable()
        if self._focused:
            self.unfocus()

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float) -> None:
        """Actualisation"""
        pass

    # ======================================== INTERNALS ========================================
    def _handle_click(self) -> None:
        """Gère le clique sur le widget"""
        self.focus()

    def _handle_outside_click(self) -> None:
        """Gère le clique en dehors du widget"""
        if self._focused:
            self.unfocus()

    def _handle_keydown(self, key: InputsManager.Input) -> None:
        """Gère l'appui d'une touche"""
        if key in self._unfocus_keys:
            self.unfocus()
            return
        self._on_keydown.trigger()
        if self._once and key not in self._ghost_keys:
            self.unfocus()

    def _apply_outside_listeners(self) -> None:
        """Met à jour les listeners de clique extérieur"""
        self._clear_outside_listeners()
        if not self._unfocus_on_outside_click:
            return
        condition = lambda: self._focused and not self._is_hovered()
        for btn in (mouse.B_LEFT, mouse.B_RIGHT, mouse.B_MIDDLE):
            listener = inputs.add_listener(
                key = btn,
                callback = self._handle_outside_click,
                condition = condition,
            )
            self._outside_listeners.add(listener)

    def _clear_outside_listeners(self) -> None:
        """Supprime les listeners de clique extérieur"""
        for listener in self._outside_listeners:
            listener.invalidate()
        self._outside_listeners.clear()

    def _is_hovered(self) -> bool:
        """Vérifie si le widget est survolé"""
        if self._owner.hover is None:
            return self._collides(mouse.get_world_position())
        return self._owner.hover.is_hovered()

    def _collides(self, point: Point) -> bool:
        """Vérifie si un point est dans le widget"""
        return self._owner.collidespoint(point)