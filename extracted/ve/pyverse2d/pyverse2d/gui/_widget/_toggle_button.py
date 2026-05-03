# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ...abc import Widget, Shape, Button
from ...math import Point
from ...shape import Rect

from numbers import Real
from typing import Callable, Any

# ======================================== WIDGET ========================================
class ToggleButton(Button):
    """Composant GUI composé: Bouton à bascule
    
    Args:
        on_widget: widget d'activation
        off_widget: widget de désactivation
        state: état initiale
        position: positionnement
        anchor: ancre relative locale
        scale: facteur de redimensionnement
        rotation: angle de rotation        
        opacity: opacité [0, 1]
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
        callback: action au basculement
        condition: condition de basculement
        id: identifiant du bouton
        give_id: donne l'identifiant à l'action
    """
    __slots__ = (
        "_on_widget", "_off_widget", "_state", "_toggle_cb", "_current",
    )

    def __init__(
            self,
            on_widget: Widget,
            off_widget: Widget = None,
            state: bool = True,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            rotation: Real = 0.0,
            opacity: Real = 1.0,
            clipping: bool = False,
            callback: Callable[[bool], Any] | None = None,
            condition: Callable[[], bool] | None = None,
            id: Any = None,
            give_id: bool = False,
        ):
        # Attributs publiques
        self._on_widget: Widget = on_widget.deepcopy()
        self._off_widget: Widget = off_widget.deepcopy() if off_widget is not None else self._on_widget.deepcopy()
        self._state: bool = state
        self._toggle_cb: Callable[[bool], Any] | None = callback
        self._current: Widget = self._on_widget if self._state else self._off_widget

        if __debug__:
            expect(self._on_widget, Widget)
            expect(self._off_widget, Widget)
            expect(self._state, bool)

        # Initialisation du bouton
        super().__init__(position, anchor, scale, rotation, opacity, clipping, callback=self._toggle, condition=condition, id=id, give_id=give_id)

        # Activation du widget courant
        self._set_widget(self._current)

    # ======================================== PROPERTIES ========================================
    @property
    def on_widget(self) -> Widget:
        """Widget d'activation

        Widget actif lorsque l'état est ``True``.
        """
        return self._on_widget
    
    @on_widget.setter
    def on_widget(self, value: Widget) -> None:
        assert isinstance(value, Widget), f"on_widget ({value}) must be a Widget"
        self._on_widget = value.deepcopy()
        if self._state:
            self._set_widget(self._on_widget)
    
    @property
    def off_widget(self) -> Widget:
        """Widget de désactivation

        Widget actif lorsque l'état est ``False``.
        """
        return self._off_widget
    
    @off_widget.setter
    def off_widget(self, value: Widget | None) -> None:
        assert isinstance(value, Widget), f"off_widget ({value}) must be a Widget"
        self._off_widget = value.deepcopy() if value is not None else self._on_widget.deepcopy()
        if not self._state:
            self._set_widget(self._off_widget)

    @property
    def state(self) -> bool:
        """Etat courant

        L'état doit être un ``bool``.
        """
        return self._state
    
    @state.setter
    def state(self, value: bool) -> None:
        assert isinstance(value, bool), f"state ({value}) must be a boolean"
        self._set_state(value)

    @property
    def callback(self) -> Callable[[bool], Any]:
        """Action au basculement

        L'action doit être un objet pouvant être appelé.
        Mettre cette propriété à ``None`` pour ne pas assigner d'action.
        """
        return self._toggle_cb
    
    @callback.setter
    def callback(self, value: Callable[[bool], Any]) -> None:
        assert value is None or callable(value), f"callback ({value}) must be a callable"
        self._toggle_cb = value

    @property
    def hitbox(self) -> Shape:
        """AABB du bouton"""
        if self._current is None:
            return Rect(1, 1)
        return self._current.hitbox

    # ======================================== PREDICATES ========================================
    def collidespoint(self, point) -> bool:
        """Vérifie la collision avec un point"""
        return self._current.collidespoint(point)

    def is_on(self) -> bool:
        """Vérifie que le basculement soit à ``True``"""
        return self._state
    
    def is_off(self) -> bool:
        """Vérifie que le basculement soit à ``False``"""
        return not self._state

    # ======================================== INTERFACE ========================================
    def copy(self) -> ToggleButton:
        """Renvoie une copie du widget"""
        return ToggleButton(
            on_widget = self._on_widget,
            off_widget = self._off_widget,
            state = self._state,
            position = self._transform.position,
            anchor = self._transform.anchor,
            scale = self._transform.scale,
            rotation = self._transform.rotation,
            opacity = self._opacity,
            clipping = self._clipping,
            callback = self._toggle_cb,
            condition = self._condition,
            id = self._id,
            give_id = self._give_id,
        )

    # ======================================== INTERNALS ========================================
    def _toggle(self, *args, **kwargs) -> None:
        """Gère le basculement"""
        self._set_state(not self._state)
        if self._toggle_cb:
            self._toggle_cb(self._state, *args, **kwargs)
    
    def _set_state(self, state: bool) -> None:
        """Change l'état courant"""
        self._state = state
        widget = self._on_widget if self._state else self._off_widget
        self._set_widget(widget)
    
    def _set_widget(self, widget: Widget) -> None:
        """Change le widget actif"""
        if self._current is not None:
            self.remove_child(self._current)
        self._current = self.add_child(widget, name="background", z=0)
        self._invalidate_scissor()
        self._invalidate_geometry()