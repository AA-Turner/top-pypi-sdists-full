# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import System
from .._world import World
from .._component import Transform, RigidBody, GroundSensor

from math import exp

# ======================================== SYSTEM ========================================
class PhysicsSystem(System):
    """Système intégrant la physique des corps dynamiques"""
    __slots__ = ()

    order = 50
    exclusive = True

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"PhysicsSystem()"

    # ======================================== LIFE CYCLE ========================================
    def update(self, world: World, dt: float):
        """Intègre la physique de tous les corps dynamiques actifs

        Args:
            world(World): monde à mettre à jour
            dt(float): delta time
        """
        for entity in world.query(RigidBody, Transform):
            rb: RigidBody = entity.get(RigidBody)
            tr: Transform = entity.get(Transform)

            if rb.is_static() or rb.is_sleeping():
                continue

            # Sauvegarde de la position pour l'anti-tunneling
            rb._save_prev(tr.x, tr.y)

            # Intégration semi-implicite d'Euler
            rb.velocity = rb.velocity + rb.acceleration * dt

            # Résistance de l'air sur X et Y
            rb._apply_damping(dt)

            # Amortissement horizontal au sol
            if entity.has(GroundSensor):
                gs: GroundSensor = entity.get(GroundSensor)
                if gs._grounded and gs._ground_damping > 0.0:
                    rb.velocity.x *= exp(-gs._ground_damping * dt)
       
            # Intégration de la position
            tr.x += rb.velocity.x * dt
            tr.y += rb.velocity.y * dt

            # Reset accélération et vérification du sleep
            rb.reset_acceleration()
            rb._tick_sleep(dt)