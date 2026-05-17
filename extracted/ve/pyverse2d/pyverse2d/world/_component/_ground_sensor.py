# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped, positive
from ...abc import Component
from ...math import Vector

from math import cos, radians
from numbers import Real
from typing import ClassVar

# ======================================== COMPONENT ========================================
class GroundSensor(Component):
    """Composant gérant le rapport entre l'entité et le sol

    Ce composant est manipulé par ``CollisionSystem`` et ``PhysicsSystem``.

    Args:
        threshold(Real, optional): composante Y minimale de la normale pour considérer sol (0 à 1)
        stability_angle(Real, optional): angle maximal en degrés auquel l'entité peut ne pas glisser (0 à 75)
        ground_damping(Real, optional): amortissement horizontal appliqué uniquement au sol
        max_step_height(Real, optional)
        coyote_time(Real, optional): durée de grâce en secondes après perte du sol
    """
    __slots__ = (
        "_threshold", "_stability_angle", "_ground_damping", "_max_step_height", "_coyote_time",
        "_coyote_elapsed", "_grounded", "_stability_ny_min", "_ground_normal",
    )

    _REQUIRES: ClassVar[tuple[str, ...]] = ("Transform", "Collider")

    def __init__(
            self,
            threshold: Real = 0.65,
            stability_angle: Real = 90.0,
            ground_damping: Real = 0.0,
            max_step_height: Real = 0.0,
            coyote_time: Real = 0.08,
        ):
        # Transtypage et vérifications
        treshold = float(treshold)
        stability_angle = abs(float(stability_angle))
        ground_damping = float(ground_damping)
        max_step_height = float(max_step_height)
        coyote_time = float(coyote_time)

        if __debug__:
            clamped(treshold)
            positive(ground_damping)
            positive(max_step_height)
            positive(coyote_time)

        # Attributs publiques
        self._threshold: float = treshold
        self._stability_angle: float = stability_angle
        self._ground_damping: float = ground_damping
        self._max_step_height: float = max_step_height
        self._coyote_time: float = coyote_time

        # Attributs internes
        self._coyote_elapsed: float = 0.0
        self._grounded: bool = False
        self._compute()

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"GroundSensor(grounded={self._grounded}, threshold={self._threshold}, stability_angle={self._stability_angle})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._threshold, self._stability_angle, self._ground_damping, self.max_step_height, self._coyote_time)
    
    def copy(self) -> GroundSensor:
        """Renvoie une copie du composant"""
        new = GroundSensor(self._threshold, self._stability_angle, self._ground_damping, self._max_step_height, self._coyote_time)
        return new
    
    # ======================================== PROPERTIES ========================================
    @property
    def threshold(self) -> float:
        """Seuil de support"""
        return self._threshold
    
    @threshold.setter
    def threshold(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            clamped(value)
        self._threshold = float(clamped(expect(value, Real)))
    
    @property
    def stability_angle(self) -> float:
        """Angle maximale grimpable"""
        return self._stability_angle
    
    @stability_angle.setter
    def stability_angle(self, value: Real) -> None:
        value = abs(float(value))
        self._stability_angle = value
        self._compute()
    
    @property
    def ground_damping(self) -> float:
        """Renvoie l'amortissement horizontal au sol"""
        return self._ground_damping

    @ground_damping.setter
    def ground_damping(self, value: Real) -> None:
        """Amortissement horizontal au sol"""
        value = float(value)
        if __debug__:
            positive(value)
        self._ground_damping = max(0.0, float(expect(value, Real)))
    
    @property
    def max_step_height(self) -> float:
        """Hauteur maximale de pas"""
        return self._max_step_height
    
    @max_step_height.setter
    def max_step_height(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._max_step_height = value

    @property
    def coyote_time(self) -> float:
        """Durée de grâce après perte du sol"""
        return self._coyote_time
    
    @coyote_time.setter
    def coyote_time(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._coyote_time = value

    # ======================================== PREDICATES ========================================
    def is_grounded(self) -> bool:
        """Vérifie que l'entité soit au sol"""
        return self._grounded
    
    # ======================================== INTERFACE ========================================
    def get_ground_normal(self) -> Vector | None:
        """Renvoie la normal de collision au sol"""
        return self._ground_normal

    # ======================================== INTERNALS ========================================
    def _compute(self) -> None:
        """Précalcul"""
        self._stability_ny_min: float = cos(radians(self._stability_angle))
        self._ground_normal: Vector | None = None

# ======================================== EXPORTS ========================================
__all__ = [
    "GroundSensor",
]