# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import HasPosition, expect, clamped, expect_callable
from ..._flag import Activity
from ...math import Vector, Point
from ...math.easing import EasingFunc, is_easing
from ...asset import Color

from abc import ABC
from dataclasses import dataclass
from numbers import Real

# ======================================== REQUEST ========================================
@dataclass(slots=True)
class AttachRequest:
    """Requête d'attache"""
    target: HasPosition
    offset: Vector
    smoothing: float

# ======================================== ABSTRACT CLASS ========================================
class LightSource(ABC):
    """Classe abstraite des sources de lumière

    Args:
        position: position
        color: couleur de la lumière émise
        intensity: intensité lumineuse
        falloff: fonction d'atténuation
        enable: activation initiale de la lumière
    """
    __slots__ = (
        "_position",
        "_color", "_intensity", "_falloff",
        "_enabled", "_attach", "_activity",
    )

    def __init__(
            self,
            position: Point = (0.0, 0.0),
            color: Color = (255, 255, 255),
            intensity: Real = 1.0,
            falloff: EasingFunc = None,
            enable: bool = True,
        ):
        # Transtyping
        position = Point(position)
        color = Color(color)
        intensity: float = float(intensity)

        # Debugging
        if __debug__:
            clamped(intensity)
            expect_callable(falloff, include_none=True)
            expect(enable, bool)

        # Attributs publiques
        self._position: Point = position
        self._color: Color = color
        self._intensity: float = intensity
        self._falloff: EasingFunc = falloff
        self._enabled: bool = enable

        # Attributs internes
        self._attach: AttachRequest | None = None
        self._activity: Activity = Activity.DEFAULT

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        """Position

        La position peut être un objet ``Point`` ou un tuple ``(x, y)``.
        """
        return self._position
    
    @position.setter
    def position(self, value: Point) -> None:
        self._position.x, self._position.y = value

    @property
    def x(self) -> float:
        """Position horizontale

        La coordonnée doit être un ``Réel``.
        """
        return self._position.x
    
    @x.setter
    def x(self, value: Real) -> None:
        self._position.x = value

    @property
    def y(self) -> float:
        """Position verticale

        La coordonnée doit être un ``Réel``.
        """
        return self._position.y
    
    @y.setter
    def y(self, value: Real) -> None:
        self._position.y = value

    @property
    def color(self) -> Color:
        """Couleur de la lumière

        La couleur peut être un objet ``Color`` ou n'importe quel tuple ``(r, g, b)``.
        Le canal alpha n'est pas pris en considération dans la couleur.
        """
        return self._color
    
    @color.setter
    def color(self, value: Color) -> None:
        self._color = Color(value)

    @property
    def intensity(self) -> float:
        """Intensité lumineuse

        L'intensité doit être un ``Réel``compris dans l'intervalle *[0, 1]*.
        Mettre cette propriété à 1.0 pour une intensité maximale.
        """
        return self._intensity
    
    @intensity.setter
    def intensity(self, value: Real) -> None:
        value = float(value)
        assert 0.0 <= value <= 1.0, f"intensity ({value}) must be within 0.0 and 1.0"
        self._intensity = value
    
    @property
    def falloff(self) -> EasingFunc:
        """Fonction d'atténuation

        La fonction doit être une ``EasingFunc``du module math.easing.
        Mettre cette propriété à None pour un éclairage constant.
        """
        return self._falloff
    
    @falloff.setter
    def falloff(self, value: EasingFunc) -> None:
        assert callable(value), f"falloff ({value}) must be an EasingFunc or None"
        self._falloff = value

    # ======================================== STATE ========================================
    def enable(self) -> None:
        """Active la lumière"""
        if self._enabled:
            return
        self._enabled = True
        self._activity = Activity.ENABLED

    def disable(self) -> None:
        """Désactive la lumière"""
        if not self._enabled:
            return
        self._enabled = False
        self._activity = Activity.DISABLED

    def toggle(self) -> None:
        """Bascule l'activation de la lumière"""
        if self._enabled:
            self.disable()
            return
        self.enable()

    def is_enabled(self) -> bool:
        """Vérifie l'activation de la lumière"""
        return self._enabled

    # ======================================== ATTACH ========================================
    def attach_to(
            self,
            target: HasPosition,
            offset: Vector = (0.0, 0.0),
            smoothing: Real = 0.0,
        ) -> None:
        """Attache la source lumineuse à un objet positionnel

        Args:
            target: cible d'attache
            offset: décalage par rapport à la cible
            smoothing: facteur de retard *[0, 1[*
        """
        offset = Vector(offset)
        smoothing = float(smoothing)
        assert 0.0 <= smoothing < 1.0, f"smoothing must be within 0.0 and 1.0 excluded"
        self._attach = AttachRequest(target, offset, smoothing)
    
    def detach(self) -> None:
        """Met fin à l'attache de la source lumineuse"""
        self._attach = None

    def is_attached(self) -> bool:
        """Vérifie si la source est attachée"""
        return self._attach is not None
    
    def attach_target(self) -> HasPosition:
        """Renvoie la cible de l'attache"""
        if self._attach is None:
            return None
        return self._attach.target

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        if self._attach is not None:
            self._update_attach(dt)
        self._update(dt)

        activity = self._activity
        self._activity = Activity.DEFAULT
        return activity

    def _update(self, dt: float) -> None:
        """Actualisation personnalisée (à override)
        
        Args:
            dt: delta-time
        """
        pass

    def _update_attach(self, dt: float) -> None:
        """Actualisation de l'attache
        
        Args:
            dt: delta-time
        """
        target = self._attach.target
        offset = self._attach.offset
        smoothing = self._attach.smoothing

        # Calcul de la position cible
        target_x, target_y = target.x + offset.x, target.y + offset.y
        t = 1 - smoothing ** dt

        # Calcul de la position intermédiaire
        x = self._position.x + (target_x - self._position.x) * t
        y = self._position.y + (target_y - self._position.y) * t

        # Mise à jour de la position
        self._position.x = x
        self._position.y = y