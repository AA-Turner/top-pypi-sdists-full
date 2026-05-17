# ======================================== IMPORTS ========================================
from __future__ import annotations

from .....shape import Circle, Ellipse, Capsule, RoundedRect

import math

# ======================================== CIRCLE ========================================
def circle_params(s: Circle, x: float, y: float, scale: float) -> tuple[float, float, float]:
    """Renvoie ``(cx, cy, r)`` en world space
    
    Args:
        s: forme
        x: position horizontale
        y: position verticale
        scale: facteur de redimensionnement
    """
    return x, y, s.radius * scale

# ======================================== ELLIPSE ========================================
def ellipse_params(s: Ellipse, x: float, y: float, scale: float, rotation: float) -> tuple[float, float, float, float]:
    """Renvoie ``(cx, cy, rx, ry)`` en world space
    
    Args:
        s: forme
        x: position horizontale
        y: position verticale
        scale: facteur de redimensionnement
        rotation: angle de rotation en degrés *(CCW)*
    """
    return x, y, s.rx * scale, s.ry * scale, math.radians(rotation)

# ======================================== CAPSULE ========================================
def capsule_params(s: Capsule, x: float, y: float, scale: float, rotation: float) -> tuple[float, float, float, float, float]:
    """Renvoie ``(ax, ay, bx, by, r)`` des extrémités de la spine en world space
    
    Args:
        s: forme
        x: position horizontale
        y: position verticale
        scale: facteur de redimensionnement
        rotation: angle de rotation en degrés *(CCW)*
    """
    r = s.radius * scale
    half_spine = s.spine * 0.5 * scale
    rad = math.radians(rotation)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    dx = -sin_r * half_spine
    dy =  cos_r * half_spine
    return x - dx, y - dy, x + dx, y + dy, r

# ======================================== ROUNDED RECT ========================================
def rounded_rect_params(s: RoundedRect, x: float, y: float, scale: float, rotation: float) -> tuple[float, float, float, float, float, float, tuple[tuple[float, float]]]:
    """Renvoie ``(cx, cy, hx, hy, r, rotation, corners_world)``
    
    Args:
        s: forme
        x: position horizontale
        y: position verticale
        scale: facteur de redimensionnement
        rotation: angle de rotation en degrés *(CCW)*
    """
    hx = s.inner_width  * 0.5 * scale
    hy = s.inner_height * 0.5 * scale
    r  = s.radius * scale
    rad = math.radians(rotation)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    local_corners = [( hx,  hy), ( hx, -hy), (-hx, -hy), (-hx,  hy)]
    corners = tuple((x + cx * cos_r - cy * sin_r, y + cx * sin_r + cy * cos_r) for cx, cy in local_corners)
    return x, y, hx, hy, r, rotation, corners

# ======================================== EXPORTS ========================================
__all__ = [
    "circle_params",
    "ellipse_params",
    "capsule_params",
    "rounded_rect_params",
]