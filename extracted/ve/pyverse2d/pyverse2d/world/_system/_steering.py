# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...abc import System
from ...math import Vector

from .._world import World
from .._component import Transform, Follow

import math

# ======================================== HELPERS ========================================
def _angle_diff(a: float, b: float) -> float:
    """Différence signée entre deux angles en degrés dans [-180, 180]"""
    return (a - b + 180.0) % 360.0 - 180.0

def _in_sector(current: float, angle: float, cone: float, cone_gap: float) -> bool:
    """Vérifie si current est dans le secteur angulaire valide"""
    if cone >= 180.0:
        return True
    abs_diff = abs(_angle_diff(current, angle))
    return cone_gap <= abs_diff <= cone

def _closest_sector_angle(current, angle, cone, cone_gap):
    if cone >= 180.0:
        return current
    if _in_sector(current, angle, cone, cone_gap):
        return current
    diff = _angle_diff(current, angle)
    abs_diff = abs(diff)
    sign = 1.0 if diff >= 0 else -1.0
    if abs_diff < cone_gap:
        return angle + sign * cone_gap
    else:
        diff_pos = abs(_angle_diff(current, angle + cone))
        diff_neg = abs(_angle_diff(current, angle - cone))
        return angle + cone if diff_pos <= diff_neg else angle - cone

# ======================================== SYSTEM ========================================
class SteeringSystem(System):
    """Système gérant le pilotage positionnel"""
    __slots__ = ()
    
    order = 10
    exclusive = True

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"SteeringSystem()"

    # ======================================== LIFE CYCLE ========================================
    def update(self, world: World, dt: float):
        """Actualisation du pilotage"""
        for entity in world.query(Follow, Transform):
            follow: Follow = entity.follow
            tr: Transform = entity.transform

            target_tr: Transform = follow.entity.transform
            target_x = target_tr.x + (follow.offset.x if follow.axis_x else 0.0)
            target_y = target_tr.y + (follow.offset.y if follow.axis_y else 0.0)

            # Vecteur de l'entité vers la cible
            dx = (target_x - tr.x) if follow.axis_x else 0.0
            dy = (target_y - tr.y) if follow.axis_y else 0.0
            dist = (dx * dx + dy * dy) ** 0.5

            # Angle de l'entité depuis la cible
            current_angle = math.degrees(math.atan2(-dy, -dx)) if dist > 1e-8 else follow.angle

            in_zone = follow.radius_min <= dist <= follow.radius_max
            in_direction = _in_sector(current_angle, follow.angle, follow.cone, follow.cone_gap)
            follow._arrived = in_zone and in_direction

            # Calcul de la direction vers le point cible le plus proche
            if not follow._arrived:
                # Angle cible
                target_angle = _closest_sector_angle(current_angle, follow.angle, follow.cone, follow.cone_gap)
                rad = math.radians(target_angle)

                # Point cible sur l'anneau
                clamped_dist = max(follow.radius_min, min(follow.radius_max, dist))
                goal_x = target_x + math.cos(rad) * clamped_dist
                goal_y = target_y + math.sin(rad) * clamped_dist

                # Vecteur vers le point cible
                dx = goal_x - tr.x
                dy = goal_y - tr.y
                dist = (dx * dx + dy * dy) ** 0.5

                if dist < 1e-8:
                    continue

                # Recalcul nx, ny
                gdist = (dx * dx + dy * dy) ** 0.5
                if gdist < 1e-8:
                    continue
                nx, ny = dx / gdist, dy / gdist

                if not in_zone:
                    if dist < follow.radius_min:
                        t = 1.0 - dist / follow.radius_min if follow.radius_min > 0.0 else 1.0
                        fx = -nx * follow.force * t
                        fy = -ny * follow.force * t
                    else:
                        span = follow.radius_max if follow.radius_max > 0.0 else 1.0
                        t = min(1.0, (dist - follow.radius_max) / span)
                        if t < 1e-6 and in_direction:
                            pass
                        else:
                            fx = nx * follow.force * t
                            fy = ny * follow.force * t

            # Cas cinématique
            rb = entity.rigid_body
            if rb is None:
                if follow._arrived:
                    continue
                t = 1.0 - follow.smoothing ** dt
                tr.x += dx * t
                tr.y += dy * t

            # Cas dynamique
            else:
                if rb.is_static():
                    continue
                if rb.is_sleeping():
                    rb.wake()

                vel = rb.velocity
                fx = fy = 0.0

                if not follow._arrived:
                    if dist < 1e-8:
                        continue

                    nx, ny = dx / dist, dy / dist

                    span = follow.radius_max if follow.radius_max > 0.0 else 1.0
                    t = min(1.0, dist / span)

                    fx = nx * follow.force * t
                    fy = ny * follow.force * t

                # Damping
                if follow.damping > 0.0:
                    fx -= vel.x * follow.damping
                    fy -= vel.y * follow.damping

                if fx == 0.0 and fy == 0.0:
                    continue

                rb.apply_force(Vector._make(fx, fy))