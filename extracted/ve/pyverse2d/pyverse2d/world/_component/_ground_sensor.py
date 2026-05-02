# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped
from ...abc import Component
from ...math import Vector

from math import cos, radians
from numbers import Real

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
    __slots__ = ("_threshold", "_stability_angle", "_ground_damping", "_max_step_height", "_coyote_time", "_coyote_elapsed", "_grounded", "_stability_ny_min", "_ground_normal")
    requires = ("Transform", "Collider")

    def __init__(self, threshold: Real = 0.65, stability_angle: Real = 90.0, ground_damping: Real = 0.0, max_step_height: Real = 0.0, coyote_time: Real = 0.08):
        self._threshold: float = float(clamped(expect(threshold, Real)))
        self._stability_angle: float = abs(float(expect(stability_angle, Real)))
        self._ground_damping: float = max(0.0, float(expect(ground_damping, Real)))
        self._max_step_height: float = max(0.0, float(expect(max_step_height, Real)))
        self._coyote_time: float = max(0.0, float(expect(coyote_time, Real)))
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
        new._coyote_elapsed = self._coyote_elapsed
        new._grounded = self._grounded
        new._stability_ny_min = self._stability_ny_min
        new._ground_normal = self._ground_normal
        return new
    
    # ======================================== GETTERS ========================================
    @property
    def threshold(self) -> float:
        """Renvoie le seuil de support"""
        return self._threshold
    
    @property
    def stability_angle(self) -> float:
        """Renvoie l'angle maximale grimpable"""
        return self._stability_angle
    
    @property
    def ground_damping(self) -> float:
        """Renvoie l'amortissement horizontal au sol"""
        return self._ground_damping
    
    @property
    def max_step_height(self) -> float:
        """Renvoie la hauteur maximale de pas"""
        return self._max_step_height

    @property
    def coyote_time(self) -> float:
        """Renvoie la durée de grâce après perte du sol"""
        return self._coyote_time
    
    @property
    def ground_normal(self) -> Vector | None:
        """Renvoie la normal de collision au sol"""
        return self._ground_normal

    # ======================================== SETTERS ========================================
    @threshold.setter
    def threshold(self, value: Real) -> None:
        """Fixe le seuil de support"""
        self._threshold = float(clamped(expect(value, Real)))

    @stability_angle.setter
    def stability_angle(self, value: Real) -> None:
        """Fixe l'angle maximal grimpable"""
        self._stability_angle = abs(float(expect(value, Real)))
        self._compute()

    @ground_damping.setter
    def ground_damping(self, value: Real) -> None:
        """Fixe l'amortissement horizontal au sol"""
        self._ground_damping = max(0.0, float(expect(value, Real)))
    
    @max_step_height.setter
    def max_step_height(self, value: Real) -> None:
        """Fixe la hauteur maximale du pas"""
        self._max_step_height = max(0.0, float(expect(value, Real)))

    @coyote_time.setter
    def coyote_time(self, value: Real) -> None:
        """Fixe la durée de grâce après perte du sol"""
        self._coyote_time = max(0.0, float(expect(value, Real)))

    # ======================================== PREDICATES ========================================
    def is_grounded(self) -> bool:
        """Vérifie que l'entité soit au sol"""
        return self._grounded

    # ======================================== INTERNALS ========================================
    def _compute(self) -> None:
        """Précalcul"""
        self._stability_ny_min: float = cos(radians(self._stability_angle))
        self._ground_normal: Vector | None = None