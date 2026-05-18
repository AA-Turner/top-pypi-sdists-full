# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import profile_section
from ...abc import System
from ...math import Vector

from .._world import World
from .._component import Transform, RigidBody

from typing import ClassVar

# ======================================== SYSTEM ========================================
class GravitySystem(System):
    """Système appliquant une force gravitationnelle sur les corps dynamiques

    Args:
        gravity: force gravitationnelle en N/kg
    """
    __slots__ = ("_gravity",)

    _ORDER: ClassVar[int] = 0

    _IS_EXCLUSIVE: ClassVar[bool] = False

    _REQUIRES: ClassVar[tuple[str, ...]] = ("PhysicsSystem",)

    def __init__(self, gravity: Vector = (0.0, -9.8)):
        # Transtypage et vérifications
        gravity = Vector(gravity)

        # Attributs publiques
        self._gravity: Vector = gravity

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"GravitySystem(gravity={self._gravity})"

    # ======================================== PROPERTIES ========================================
    @property
    def gravity(self) -> Vector:
        """Vecteur gravitationnel en N/kg
        
        Le vecteur peut être un objet ``Vector`` ou n'import quel tuple ``(vx, vy)``.
        """
        return self._gravity

    @gravity.setter
    def gravity(self, value: Vector):
        value = Vector(value)
        self._gravity = value

    # ======================================== LIFE CYCLE ========================================
    @profile_section("world.gravity.update")
    def update(self, world: World, dt: float):
        """Applique la force gravitationnelle sur tous les corps dynamiques

        Args:
            world: monde à mettre à jour
            dt: delta-time
        """
        for entity in world.query(RigidBody, Transform):
            rb: RigidBody = entity.get(RigidBody)
            if rb.is_static() or not rb.is_gravitational():
                continue
            rb.apply_acceleration(self._gravity * rb.gravity_scale)

# ======================================== EXPORTS ========================================
__all__ = [
    "GravitySystem",
]