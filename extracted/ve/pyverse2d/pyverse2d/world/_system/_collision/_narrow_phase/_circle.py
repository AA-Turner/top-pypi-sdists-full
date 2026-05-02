# ======================================== IMPORTS ========================================
from __future__ import annotations

from .....math import Vector
from .....abc import Shape
from .....shape import Circle, Ellipse, Capsule

from .._registry import Contact, register

from ._prim_transform import circle_params, ellipse_params, capsule_params
from ._helper import closest_pt_on_seg, closest_pt_on_ellipse

from math import sqrt, cos, sin

# ======================================== Circle × Circle ========================================
@register(Circle, Circle)
def circle_circle(sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float, sb: Shape, bx: float, by: float, scale_b: float, rot_b: float):
    """Vérifie la collision entre ``Circle`` et ``Circle``"""
    _, _, ra = circle_params(sa, ax, ay, scale_a)
    _, _, rb = circle_params(sb, bx, by, scale_b)
    dx, dy = ax - bx, ay - by
    dist_sq = dx*dx + dy*dy
    radii = ra + rb
    if dist_sq >= radii * radii:
        return None
    dist = sqrt(dist_sq) or 1e-8
    return Contact(Vector._make(dx/dist, dy/dist), radii - dist)

# ======================================== Circle × Ellipse ========================================
@register(Circle, Ellipse)
def circle_ellipse(sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float, sb: Shape, bx: float, by: float, scale_b: float, rot_b: float):
    """Vérifie la collision entre ``Circle`` et ``Ellipse``"""
    _, _, r = circle_params(sa, ax, ay, scale_a)
    ex, ey, rx, ry, rot_rad = ellipse_params(sb, bx, by, scale_b, rot_b)
    cos_r, sin_r = cos(-rot_rad), sin(-rot_rad)
    dx, dy = ax - ex, ay - ey
    clx =  dx * cos_r - dy * sin_r
    cly =  dx * sin_r + dy * cos_r
    inside = (clx / rx) ** 2 + (cly / ry) ** 2 <= 1.0
    qlx, qly = closest_pt_on_ellipse(0.0, 0.0, rx, ry, clx, cly)
    ddx, ddy = clx - qlx, cly - qly
    dist = sqrt(ddx * ddx + ddy * ddy) or 1e-8
    cos_w, sin_w = cos(rot_rad), sin(rot_rad)
    nx = (ddx / dist) * cos_w - (ddy / dist) * sin_w
    ny = (ddx / dist) * sin_w + (ddy / dist) * cos_w
    if inside:
        return Contact(Vector._make(nx, ny), r + dist)
    if dist >= r:
        return None
    return Contact(Vector._make(nx, ny), r - dist)

# ======================================== Circle × Capsule ========================================
@register(Circle, Capsule)
def circle_capsule(sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float, sb: Shape, bx: float, by: float, scale_b: float, rot_b: float):
    """Vérifie la collision entre ``Circle`` et ``Capsule``"""
    _, _, r = circle_params(sa, ax, ay, scale_a)
    cap_ax, cap_ay, cap_bx, cap_by, cap_r = capsule_params(sb, bx, by, scale_b, rot_b)
    spine_dx, spine_dy = cap_bx - cap_ax, cap_by - cap_ay
    qx, qy = closest_pt_on_seg(cap_ax, cap_ay, spine_dx, spine_dy, ax, ay)
    dx, dy = ax - qx, ay - qy
    dist_sq = dx*dx + dy*dy
    radii = r + cap_r
    if dist_sq >= radii * radii:
        return None
    dist = sqrt(dist_sq) or 1e-8
    return Contact(Vector._make(dx/dist, dy/dist), radii - dist)

# ======================================== EXPORTS ========================================
__all__ = [
    "circle_circle",
    "circle_ellipse",
    "circle_capsule",
]