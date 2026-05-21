# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import HasPosition, positive, expect, clamped
from ..._flag import Activity
from ..._core import Positionable
from ...abc import PostFxEffect, Shape
from ...math import Vector, Point
from ...shape import Circle, Rect

from dataclasses import dataclass
from typing import Type
from numbers import Real

# ======================================== CONSTANTS ========================================
_SUPPORTED_SHAPES: frozenset[type] = frozenset({Circle, Rect})

# ======================================== ATTACH REQUEST ========================================
@dataclass(slots=True)
class _AttachRequest:
    """Requête d'attache interne

    Args:
        target: cible positionnelle
        offset: décalage par rapport à la cible
        smoothing: atténuation du suivi *[0, 1[*
    """
    target: HasPosition
    offset: Vector
    smoothing: float

# ======================================== ZONE ========================================
class PostFxZone(Positionable):
    """Zone d'effet post-processing

    Args:
        shape: forme de la zone *(``Circle`` ou ``Rect``)*, ou ``None`` pour unbounded
        position: position monde du centre de la zone
        blend: distance de fondu en pixels depuis le bord de la shape *(>= 0)*
        enabled: activation initiale
    """
    __slots__ = (
        "_shape", "_blend",
        "_unbounded",
        "_enabled", "_activity",
        "_effects", "_order",
        "_attach",
    )

    def __init__(
        self,
        shape: Shape | None = None,
        position: Point = (0.0, 0.0),
        blend: Real = 0.0,
        enabled: bool = True,
    ):
        # Initialisation de la position
        Positionable.__init__(self, position)

        # Transtypage et vérifications
        blend = float(blend)
        enabled = bool(enabled)

        if __debug__:
            if shape is not None and type(shape) not in _SUPPORTED_SHAPES: raise TypeError(f"Shape {type(shape).__name__} not supported")
            positive(blend)

        # Attributs
        self._shape: Shape | None = shape
        self._blend: float = blend
        self._unbounded: bool = shape is None
        self._enabled: bool = enabled
        self._activity: Activity = Activity.DEFAULT

        # Effets
        self._effects: dict[Type[PostFxEffect], PostFxEffect] = {}
        self._order: list[Type[PostFxEffect]] = []

        # Attache
        self._attach: _AttachRequest | None = None

    # ======================================== PROPERTIES ========================================
    @property
    def shape(self) -> Shape | None:
        """Forme de la zone *(lecture seule)*

        Mettre cette propriété à ``None`` si la zone est unbounded.
        """
        return self._shape

    @property
    def blend(self) -> float:
        """Distance de fondu en pixels depuis le bord de la shape *(>= 0)*"""
        return self._blend

    @blend.setter
    def blend(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._blend = value

    # ======================================== PREDICATES ========================================
    def is_bounded(self) -> bool:
        """Vérifie que la zone possède une shape délimitée"""
        return not self._unbounded

    def is_unbounded(self) -> bool:
        """Vérifie que la zone couvre la totalité du framebuffer"""
        return self._unbounded

    def is_enabled(self) -> bool:
        """Vérifie l'activation de la zone"""
        return self._enabled

    # ======================================== STATE ========================================
    def enable(self) -> None:
        """Active la zone"""
        if self._enabled:
            return
        self._enabled = True
        self._activity = Activity.ENABLED

    def disable(self) -> None:
        """Désactive la zone"""
        if not self._enabled:
            return
        self._enabled = False
        self._activity = Activity.DISABLED

    def toggle(self) -> None:
        """Bascule l'activation de la zone"""
        if self._enabled:
            self.disable()
        else:
            self.enable()

    # ======================================== EFFECTS ========================================
    def add_effect(self, effect: PostFxEffect) -> None:
        """Ajoute un effet en fin de chaîne

        Args:
            effect: effet à ajouter
        """
        if __debug__:
            expect(effect, PostFxEffect)
        t = type(effect)
        if t in self._effects:
            raise RuntimeError(f"This zone has already a {t.__name__} effect")
        self._effects[t] = effect
        self._order.append(t)

    def remove_effect(self, effect_type: Type[PostFxEffect]) -> PostFxEffect:
        """Retire un effet de la chaîne

        Args:
            effect_type: type de l'effet à retirer

        Returns:
            PostFxEffect: l'effet retiré
        """
        if effect_type not in self._effects:
            raise RuntimeError(f"This zone has already a {effect_type.__name__} effect")
        self._order.remove(effect_type)
        return self._effects.pop(effect_type)

    def replace_effect(self, effect: PostFxEffect) -> None:
        """Remplace un effet existant par un nouveau

        Args:
            effect: nouvel effet du même type
        """
        if __debug__:
            expect(effect, PostFxEffect)
        t = type(effect)
        if t not in self._effects:
            raise RuntimeError(f"This zone has no effect {t.__name__}")
        self._effects[t] = effect

    def move_effect(self, effect_type: Type[PostFxEffect], index: int) -> None:
        """Déplace un effet à une position donnée dans la chaîne

        Args:
            effect_type: type de l'effet à déplacer
            index: nouvelle position *(0 = premier appliqué)*
        """
        if effect_type not in self._effects:
            raise RuntimeError(f"This zone has no effect {effect_type.__name__}")
        self._order.remove(effect_type)
        self._order.insert(int(index), effect_type)

    def get_effect(self, effect_type: Type[PostFxEffect]) -> PostFxEffect | None:
        """Renvoie un effet ou ``None`` s'il n'est pas présent

        Args:
            effect_type: type de l'effet
        """
        return self._effects.get(effect_type)

    def get_effects(self) -> tuple[PostFxEffect, ...]:
        """Renvoie les effets actifs dans leur ordre d'application"""
        return tuple(self._effects[t] for t in self._order)

    def has_effect(self, effect_type: Type[PostFxEffect]) -> bool:
        """Vérifie la présence d'un effet

        Args:
            effect_type: type de l'effet à vérifier
        """
        return effect_type in self._effects

    # ======================================== ATTACH ========================================
    def attach_to(
        self,
        target: HasPosition,
        offset: Vector = (0.0, 0.0),
        smoothing: Real = 0.0,
    ) -> None:
        """Attache la zone à un objet positionnel

        Args:
            target: cible d'attache
            offset: décalage par rapport à la cible
            smoothing: facteur de retard *[0, 1[*
        """
        offset = Vector(offset)
        smoothing = float(smoothing)
        if __debug__:
            clamped(smoothing, include_max=False)
        self._attach = _AttachRequest(target, offset, smoothing)

    def detach(self) -> None:
        """Met fin à l'attache de la zone"""
        self._attach = None

    def is_attached(self) -> bool:
        """Vérifie si la zone est attachée"""
        return self._attach is not None

    def attach_target(self) -> HasPosition | None:
        """Renvoie la cible de l'attache"""
        return self._attach.target if self._attach is not None else None

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> Activity:
        """Actualisation

        Args:
            dt: delta-time

        Returns:
            Activity: changement d'état pour ce frame
        """
        if self._attach is not None:
            self._update_attach(dt)

        activity = self._activity
        self._activity = Activity.DEFAULT
        return activity

    def _update_attach(self, dt: float) -> None:
        """Actualisation du suivi de cible

        Args:
            dt: delta-time
        """
        target = self._attach.target
        offset = self._attach.offset
        smoothing = self._attach.smoothing

        target_x = target.x + offset.x
        target_y = target.y + offset.y
        t = 1.0 - smoothing ** dt

        self._position.x += (target_x - self._position.x) * t
        self._position.y += (target_y - self._position.y) * t

# ======================================== EXPORTS ========================================
__all__ = [
    "PostFxZone",
]