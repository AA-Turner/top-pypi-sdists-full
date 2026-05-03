# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, expect_callable
from ...math import Point

from ._widget import Widget

from numbers import Real
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..._rendering import Pipeline
    from ...gui import RenderContext

# ======================================== WIDGET ========================================
class Button(Widget):
    """Classe abstraite des composants GUI: Bouton

    Args:
        position: positionnement
        anchor: ancre relative locale
        scale: facteur de redimensionnement
        rotation: angle de rotation
        opacity: opacité [0, 1]
        clipping: rendu des widgets enfants strictement dans le AABB de la hitbox
        callback: action au clique
        condition: condition d'action
        id: identifiant du bouton
        give_id: passe l'identifiant à l'action
    """
    __slots__ = (
        "_callback", "_condition", "_id", "_give_id",
    )

    _ACTION_NAME: str = "_default"

    def __init__(
            self,
            position: Point = (0.0, 0.0),
            anchor: Point = (0.5, 0.5),
            scale: Real = 1.0,
            rotation: Real = 0.0,
            opacity: Real = 1.0,
            clipping: bool = False,
            callback: Callable | None = None,
            condition: Callable | None = None,
            id: Any = None,
            give_id: bool = False,
        ):
        if __debug__:
            expect_callable(callback, include_none=True, arg="callback")
            expect_callable(condition, include_none=True, arg="condition")
            expect(give_id, bool)

        # Attributs publiques
        self._callback: Callable = callback
        self._condition: Callable = condition
        self._id: Any = id
        self._give_id: bool = give_id

        # Initialisation du widget
        super().__init__(position, anchor, scale, rotation, opacity, clipping=clipping)

        # Comportements prédéfinis
        from ...gui import HoverBehavior, ClickBehavior
        self.add_behavior(HoverBehavior())
        self.add_behavior(ClickBehavior())

        # Application du callback
        self._apply_callback()

    # ======================================== PROPERTIES ========================================
    @property
    def callback(self) -> Callable | None:
        """Action au clique

        L'action doit être un objet pouvant être appelé.
        Mettre cette propriété à ``None`` pour ne pas assigner d'action.
        """
        return self._callback

    @callback.setter
    def callback(self, value: Callable | None) -> None:
        assert value is None or callable(value), f"callback ({value}) must be a callable"
        if value == self._callback:
            return
        with self._refresh:
            self._callback = value

    @property
    def condition(self) -> Callable | None:
        """Condition d'action

        Cette propriété ajoute une condition à l'appel de l'action lors du clique.
        La condition doit être un objet pouvant être appelé.
        Mettre à ``None`` pour ne pas avoir de condition.
        """
        return self._condition

    @condition.setter
    def condition(self, value: Callable | None) -> None:
        assert value is None or callable(value), f"condition ({value}) must be a callable"
        if value == self._condition:
            return
        with self._refresh:
            self._condition = value

    @property
    def id(self) -> Any:
        """Identifiant du bouton

        L'indentifiant peut être n'importe quoi.
        """
        return self._id

    @id.setter
    def id(self, value: Any) -> None:
        with self._refresh:
            self._id = value

    @property
    def give_id(self) -> bool:
        """Donne l'identifiant à l'action

        Activer cette propriété passera un kwarg ``id`` au callback.
        """
        return self._give_id

    @give_id.setter
    def give_id(self, value: bool) -> None:
        assert isinstance(value, bool), f"give_id ({value}) must be a boolean"
        with self._refresh:
            self._give_id = value

    # ======================================== PREDICATES ========================================
    def is_hovered(self) -> bool:
        """Vérifie que le widget soit survolé"""
        return self.hover.is_hovered()

    # ======================================== LIFE CYCLE ========================================
    def _update(self, dt: float):
        """Actualisation"""
        ...

    def _draw(self, pipeline: Pipeline, context: RenderContext):
        """Affichage"""
        ...

    def _destroy(self):
        """Libère les ressources pyglet"""
        ...

    # ======================================== INTERNALS ========================================
    def _apply_callback(self) -> None:
        """Applique le callback"""
        if self._callback is not None:
            self.click.add(name=self._ACTION_NAME, callback=self._callback, kwargs={"id": self._id} if self._give_id else None, condition=self._condition)

    def _remove_callback(self) -> None:
        """Retire le callback"""
        if self.click.has(self._ACTION_NAME):
            self.click.remove(self._ACTION_NAME)

    def _refresh(self):
        """Contexte d'actualisation de l'action"""
        self._remove_callback()
        try:
            yield
        finally:
            self._apply_callback()