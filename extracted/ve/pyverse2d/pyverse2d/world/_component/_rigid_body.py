# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, clamped, positive
from ...abc import Component
from ...math import Vector

from numbers import Real
from math import exp

# ======================================== CONSTANTES ========================================
_SLEEP_THRESHOLD = 0.5      # vitesse (m/s) en dessous de laquelle le timer démarre
_SLEEP_DELAY = 0.5          # secondes consécutives sous le seuil avant mise en veille

# ======================================== COMPONENT ========================================
class RigidBody(Component):
    """Composant gérant un corps dynamique

    Ce composant est manipulé par ``PhysicsSystem``, ``CollisionSystem`` et ``SteeringSystem``.

    Args:
        mass(Real, optional): masse du corps en kg (0 ou inf pour un corps statique)
        friction(Real, optional): résistance au glissement [0, 1]
        restitution(Real, optional): facteur de rebond [0, 1]
        gravity(bool, optional): soumission à la gravité
        gravity_scale(Real, optional): facteur de gravité
        linear_damping(Real, optional): résistance de l'air (0 = aucune)
    """
    __slots__ = ("_mass", "_friction", "_restitution", "_gravity", "_gravity_scale", "_linear_damping", "_velocity", "_acceleration", "_prev_x", "_prev_y", "_sleeping", "_sleep_timer")
    requires = ("Transform",)

    def __init__(
            self,
            mass: Real = 0.0,
            friction: Real = 0.5,
            restitution: Real = 0.0,
            gravity: bool = True,
            gravity_scale: Real = 1.0,
            linear_damping: Real = 0.0,
        ):
        self._mass = float(positive(expect(mass, Real)))
        self._friction = float(clamped(expect(friction, Real)))
        self._restitution = float(positive(expect(restitution, Real)))
        self._gravity = expect(gravity, bool)
        self._gravity_scale = float(expect(gravity_scale, Real))
        self._linear_damping = float(max(0.0, expect(linear_damping, Real)))
        self._velocity = Vector(0.0, 0.0)
        self._acceleration = Vector(0.0, 0.0)
        self._prev_x = 0.0
        self._prev_y = 0.0
        self._sleeping = False
        self._sleep_timer = 0.0

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

    # ======================================== GETTERS ========================================
    @property
    def mass(self) -> float:
        """Renvoie la masse du corps en kg"""
        return self._mass

    @property
    def friction(self) -> float:
        """Renvoie le facteur de friction du corps"""
        return self._friction

    @property
    def restitution(self) -> float:
        """Renvoie le facteur de restitution du corps"""
        return self._restitution

    @property
    def gravity_scale(self) -> float:
        """Renvoie le facteur de gravité"""
        return self._gravity_scale

    @property
    def linear_damping(self) -> float:
        """Renvoie le coefficient de résistance de l'air"""
        return self._linear_damping

    @property
    def velocity(self) -> Vector:
        """Renvoie la vélocité du corps"""
        return self._velocity

    @property
    def acceleration(self) -> Vector:
        """Renvoie l'accélération du corps"""
        return self._acceleration

    @property
    def prev_x(self) -> float:
        """Renvoie la position x de la frame précédente"""
        return self._prev_x

    @property
    def prev_y(self) -> float:
        """Renvoie la position y de la frame précédente"""
        return self._prev_y

    @property
    def sleep_timer(self) -> float:
        """Renvoie le temps cumulé sous le seuil de vélocité en secondes"""
        return self._sleep_timer

    # ======================================== SETTERS ========================================
    @mass.setter
    def mass(self, value: Real):
        self._mass = float(positive(expect(value, Real)))

    @friction.setter
    def friction(self, value: Real):
        self._friction = float(clamped(expect(value, Real)))

    @restitution.setter
    def restitution(self, value: Real):
        self._restitution = float(positive(expect(value, Real)))

    @gravity_scale.setter
    def gravity_scale(self, value: Real):
        self._gravity_scale = float(expect(value, Real))

    @linear_damping.setter
    def linear_damping(self, value: Real):
        self._linear_damping = float(max(0.0, expect(value, Real)))

    @velocity.setter
    def velocity(self, value):
        self._velocity = Vector(value)

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = Vector(value)

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
        """
        Applique une accélération directement, sans réveiller le corps

        Args:
            acc(Vector): accélération à appliquer en px/s²
        """
        if self.is_static() or self._sleeping:
            return
        self._acceleration = self._acceleration + Vector(acc)

    def apply_force(self, force: Vector):
        """
        Applique une force au corps et le réveille si nécessaire

        Args:
            force(Vector): force à appliquer en N
        """
        if self.is_static():
            return
        if self._sleeping:
            self.wake()
        self._acceleration = self._acceleration + Vector(force) * (1.0 / self._mass)

    def apply_impulse(self, impulse: Vector):
        """
        Applique une impulsion instantanée, indépendante du dt

        Args:
            impulse(Vector): impulsion en kg·m/s
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
        """Sauvegarde la position courante comme position précédente"""
        self._prev_x = x
        self._prev_y = y

    def _apply_damping(self, dt: float):
        """Applique la résistance de l'air via décroissance exponentielle"""
        if self._linear_damping == 0.0:
            return
        factor = exp(-self._linear_damping * dt)
        self._velocity = self._velocity * factor

    def _tick_sleep(self, dt: float):
        vx = self._velocity.x
        vy = self._velocity.y
        speed_sq = vx * vx + vy * vy
        if speed_sq < _SLEEP_THRESHOLD * _SLEEP_THRESHOLD:
            self._sleep_timer += dt
            if self._sleep_timer >= _SLEEP_DELAY:
                self.sleep()
        else:
            self._sleep_timer = 0.0

    # ======================================== PUBLIC METHODS ========================================
    def enable_gravity(self):
        """Active la gravité"""
        self._gravity = True

    def disable_gravity(self):
        """Désactive la gravité"""
        self._gravity = False