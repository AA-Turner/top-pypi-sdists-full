# ======================================== IMPORTS ========================================
from __future__ import annotations

from .....math import Vector
from .....abc import Shape
from .....shape import Capsule

from .._registry import Contact, register

from ._prim_transform import capsule_params
from ._helper import closest_pt_on_seg, closest_pt_seg_to_seg

from math import sqrt

# ======================================== Capsule × Capsule ========================================
@register(Capsule, Capsule)
def capsule_capsule(sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float, sb: Shape, bx: float, by: float, scale_b: float, rot_b: float):
    """Vérifie la collision entre ``Capsule`` et ``Capsule``"""
    a_ax, a_ay, a_bx, a_by, ra = capsule_params(sa, ax, ay, scale_a, rot_a)
    b_ax, b_ay, b_bx, b_by, rb = capsule_params(sb, bx, by, scale_b, rot_b)
    a_dx, a_dy = a_bx - a_ax, a_by - a_ay
    b_dx, b_dy = b_bx - b_ax, b_by - b_ay
    px, py = closest_pt_seg_to_seg(a_ax, a_ay, a_dx, a_dy, b_ax, b_ay, b_dx, b_dy)
    qx, qy = closest_pt_on_seg(b_ax, b_ay, b_dx, b_dy, px, py)
    dx = px - qx
    dy = py - qy
    dist_sq = dx * dx + dy * dy
    radii = ra + rb
    if dist_sq >= radii * radii:
        return None
    dist = sqrt(dist_sq) or 1e-8
    return Contact(Vector._make(dx / dist, dy / dist), radii - dist)

# ======================================== EXPORTS ========================================
__all__ = [
    "capsule_capsule",
]