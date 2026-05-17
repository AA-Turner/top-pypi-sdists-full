# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped, positive
from ...abc import Component
from ...math import Vector

from numbers import Real
from math import exp
from typing import ClassVar

# ======================================== CONSTANTES ========================================
_SLEEP_THRESHOLD = 0.5  # vitesse (u/s) en dessous de laquelle le timer démarre
_SLEEP_DELAY = 0.5      # secondes consécutives sous le seuil avant mise en veille

# ======================================== COMPONENT ========================================
class RigidBody(Component):
    """Composant gérant un corps dynamique

    Ce composant est manipulé par ``PhysicsSystem``, ``CollisionSystem`` et ``SteeringSystem``.

    Args:
        mass: masse du corps en kg *(0 ou inf pour un corps statique)*
        friction: résistance au glissement *[0, 1]*
        restitution: facteur de rebond *[0, 1]*
        gravity: soumission à la gravité
        gravity_scale: facteur de gravité
        linear_damping: résistance de l'air *(0 = aucune)*
    """
    __slots__ = (
        "_mass", "_friction", "_restitution",
        "_gravity", "_gravity_scale", "_linear_damping",
        "_velocity", "_acceleration", "_prev_x", "_prev_y",
        "_sleeping", "_sleep_timer",
    )
    
    _REQUIRES: ClassVar[tuple[str, ...]] = ("Transform",)

    def __init__(
            self,
            mass: Real = 0.0,
            friction: Real = 0.5,
            restitution: Real = 0.0,
            gravity: bool = True,
            gravity_scale: Real = 1.0,
            linear_damping: Real = 0.0,
        ):
        # Transtypage et vérifications
        mass = float(mass)
        friction = float(friction)
        restitution = float(restitution)
        gravity = bool(gravity)
        gravity_scale = float(gravity_scale)
        linear_damping = float(linear_damping)
        
        if __debug__:
            positive(mass)
            clamped(friction)
            positive(restitution)
            positive(linear_damping)

        # Attributs publiques
        self._mass = mass
        self._friction = friction
        self._restitution = restitution
        self._gravity = gravity
        self._gravity_scale = gravity_scale
        self._linear_damping = linear_damping

        # Attributs internes
        self._velocity: Vector = Vector(0.0, 0.0)
        self._acceleration: Vector = Vector(0.0, 0.0)
        self._prev_x: float = 0.0
        self._prev_y: float = 0.0
        self._sleeping: bool = False
        self._sleep_timer: float = 0.0

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"RigidBody(mass={self._mass}, friction={self._friction}, restitution={self._restitution})"

    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._mass, self._friction, self._restitution, self._gravity, self._gravity_scale, self._linear_damping)
    
    def copy(self) -> RigidBody:
        """Renvoie une copie du composant"""
        new = RigidBody(self._mass, self._friction, self._restitution, self._gravity, self._gravity_scale, self._linear_damping)
        new._velocity = self._velocity
        new._acceleration = self._acceleration
        new._prev_x = self._prev_x
        new._prev_y = self._prev_y
        new._sleeping = self._sleeping
        new._sleep_timer = self._sleep_timer
        return new

    # ======================================== PROPERTIES ========================================
    @property
    def mass(self) -> float:
        """Masse du corps en kg"""
        return self._mass
    
    @mass.setter
    def mass(self, value: Real):
        value = float(value)
        if __debug__:
            positive(value)
        self._mass = value

    @property
    def friction(self) -> float:
        """Facteur de friction du corps"""
        return self._friction
    
    @friction.setter
    def friction(self, value: Real):
        value = float(value)
        if __debug__:
            clamped(value)
        self._friction = value

    @property
    def restitution(self) -> float:
        """Facteur de restitution du corps"""
        return self._restitution
    
    @restitution.setter
    def restitution(self, value: Real):
        value = float(value)
        if __debug__:
            positive(value)
        self._restitution = value

    @property
    def gravity(self) -> bool:
        """Soumission à la gravité"""
        return self._gravity
    
    @gravity.setter
    def gravity(self, value: bool) -> None:
        value = bool(value)
        self._gravity = value

    @property
    def gravity_scale(self) -> float:
        """Facteur de gravité"""
        return self._gravity_scale
    
    @gravity_scale.setter
    def gravity_scale(self, value: Real):
        value = float(value)
        self._gravity_scale = value

    @property
    def linear_damping(self) -> float:
        """Coefficient de résistance de l'air"""
        return self._linear_damping
    
    @linear_damping.setter
    def linear_damping(self, value: Real):
        value = float(value)
        if __debug__:
            positive(value)
        self._linear_damping = value

    @property
    def velocity(self) -> Vector:
        """Vélocité du corps"""
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        self._velocity.x, self._velocity.y = value

    @property
    def acceleration(self) -> Vector:
        """Accélération du corps"""
        return self._acceleration
    
    @acceleration.setter
    def acceleration(self, value):
        self._acceleration.x, self._acceleration.y = value

    @property
    def prev_x(self) -> float:
        """Position x de la frame précédente *(lecture seule)*"""
        return self._prev_x

    @property
    def prev_y(self) -> float:
        """Position y de la frame précédente *(lecture seule)*"""
        return self._prev_y

    @property
    def sleep_timer(self) -> float:
        """Temps cumulé sous le seuil de vélocité en secondes *(lecture seule)*"""
        return self._sleep_timer

    # ======================================== PREDICATES ========================================
    def is_static(self) -> bool:
        """Vérifie si le corps est statique"""
        return self._mass == 0 or self._mass == float("inf")

    def is_gravitational(self) -> bool:
        """Vérifie la soumission à la gravité"""
        return self._gravity

    def is_sleeping(self) -> bool:
        """Vérifie si le corps est en veille"""
        return self._sleeping

    # ======================================== SLEEP ========================================
    def sleep(self):
        """Met le corps en veille et remet sa vélocité et son timer à zéro"""
        self._sleeping = True
        self._sleep_timer = 0.0
        self._velocity = Vector(0.0, 0.0)
        self._acceleration = Vector(0.0, 0.0)

    def wake(self):
        """Réveille le corps et remet le timer à zéro"""
        self._sleeping = False
        self._sleep_timer = 0.0

    # ======================================== FORCES ========================================
    def apply_acceleration(self, acc: Vector):
        """Applique une accélération directement, sans réveiller le corps

        Args:
            acc: accélération à appliquer en u/s²
        """
        if self.is_static() or self._sleeping:
            return
        self._acceleration = self._acceleration + Vector(acc)

    def apply_force(self, force: Vector):
        """Applique une force au corps et le réveille si nécessaire

        Args:
            force: force à appliquer en N
        """
        if self.is_static():
            return
        if self._sleeping:
            self.wake()
        self._acceleration = self._acceleration + Vector(force) * (1.0 / self._mass)

    def apply_impulse(self, impulse: Vector):
        """Applique une impulsion instantanée, indépendante du dt

        Args:
            impulse: impulsion en kg·u/s
        """
        if self.is_static():
            return
        if self._sleeping:
            self.wake()
        self._velocity = self._velocity + Vector(impulse) * (1.0 / self._mass)

    def reset_acceleration(self):
        """Remet l'accélération à zéro"""
        self._acceleration = Vector(0.0, 0.0)

    # ======================================== INTERNALS ========================================
    def _save_prev(self, x: float, y: float):
        """Sauvegarde la position courante comme position précédente
        
        Args:
            x: position horizontale
            y: position verticale
        """
        self._prev_x = x
        self._prev_y = y

    def _apply_damping(self, dt: float):
        """Applique la résistance de l'air via décroissance exponentielle
        
        Args:
            dt: delta-time
        """
        if self._linear_damping == 0.0:
            return
        factor = exp(-self._linear_damping * dt)
        self._velocity = self._velocity * factor

    def _tick_sleep(self, dt: float):
        """Mise à jour du sommeil

        Args:
            dt: delta-time
        """
        vx = self._velocity.x
        vy = self._velocity.y
        speed_sq = vx * vx + vy * vy
        if speed_sq < _SLEEP_THRESHOLD * _SLEEP_THRESHOLD:
            self._sleep_timer += dt
            if self._sleep_timer >= _SLEEP_DELAY:
                self.sleep()
        else:
            self._sleep_timer = 0.0

# ======================================== EXPORTS ========================================
__all__ = [
    "RigidBody",
]