# ======================================== IMPORTS ========================================
from __future__ import annotations

from math import cos, sin, atan2, radians, sqrt
import numpy as np
from numpy.typing import NDArray

# ======================================== CAPSULE ========================================
def closest_pt_on_seg(sx: float, sy: float, sdx: float, sdy: float, px: float, py: float) -> tuple[float, float]:
    """Point le plus proche de ``(px,py)`` sur le segment *(sx,sy) -> (sx+sdx,sy+sdy)*"""
    len_sq = sdx * sdx + sdy * sdy
    if len_sq < 1e-10:
        return sx, sy
    t = max(0.0, min(1.0, ((px - sx) * sdx + (py - sy) * sdy) / len_sq))
    return sx + t * sdx, sy + t * sdy

def closest_pt_seg_to_seg(ax: float, ay: float, adx: float, ady: float, bx: float, by: float, bdx: float, bdy: float) -> tuple[float, float]:
    """Point le plus proche sur le segment ``A`` du segment ``B``"""
    a_len_sq = adx * adx + ady * ady
    b_len_sq = bdx * bdx + bdy * bdy
    rx, ry = ax - bx, ay - by
    e = rx * bdx + ry * bdy
    f = adx * bdx + ady * bdy

    if a_len_sq < 1e-10 and b_len_sq < 1e-10:
        return ax, ay
    if a_len_sq < 1e-10:
        s = max(0.0, min(1.0, e / b_len_sq))
        return bx + s * bdx, by + s * bdy
    c = rx * adx + ry * ady
    if b_len_sq < 1e-10:
        t = max(0.0, min(1.0, -c / a_len_sq))
        return ax + t * adx, ay + t * ady
    denom = a_len_sq * b_len_sq - f * f
    t = max(0.0, min(1.0, (f * e - c * b_len_sq) / denom)) if abs(denom) > 1e-10 else 0.0
    s = max(0.0, min(1.0, (f * t + e) / b_len_sq))
    t = max(0.0, min(1.0, (f * s - c) / a_len_sq))
    return ax + t * adx, ay + t * ady

# ======================================== VERTEX ========================================
def point_in_convex_poly(px: float, py: float, pts: NDArray[np.float32]) -> bool:
    """Vérifie si ``(px,py)`` est à l'intérieur d'un polygone convexe"""
    p = np.array([px, py], dtype=np.float32)
    v1 = pts
    v2 = np.roll(pts, -1, axis=0)
    cross = (v2[:, 0] - v1[:, 0]) * (p[1] - v1[:, 1]) - (v2[:, 1] - v1[:, 1]) * (p[0] - v1[:, 0])
    mask = np.abs(cross) >= 1e-6
    if not np.any(mask):
        return False
    signs = cross[mask] > 0
    return np.all(signs) or not np.any(signs)
# ======================================== ELLIPSE ========================================
def to_ellipse_local(px: float, py: float, ex: float, ey: float, rot_rad: float) -> tuple[float, float]:
    """Ramène ``(px,py)`` dans l'espace local de l'ellipse"""
    dx, dy = px - ex, py - ey
    cos_r, sin_r = cos(-rot_rad), sin(-rot_rad)
    return dx * cos_r - dy * sin_r, dx * sin_r + dy * cos_r

def from_ellipse_local(lx: float, ly: float, ex: float, ey: float, rot_rad: float) -> tuple[float, float]:
    """Repasse en world space"""
    cos_r, sin_r = cos(rot_rad), sin(rot_rad)
    return ex + lx * cos_r - ly * sin_r, ey + lx * sin_r + ly * cos_r

def closest_pt_on_ellipse(cx: float, cy: float, rx: float, ry: float, px: float, py: float) -> tuple[float, float]:
    """Point le plus proche sur l'ellipse ``(cx,cy,rx,ry)`` du point ``(px,py)``"""
    lx = px - cx
    ly = py - cy
    if abs(lx) < 1e-12 and abs(ly) < 1e-12:
        return cx + rx, cy
    t = atan2(ly * rx, lx * ry)
    for _ in range(25):
        ct, st = cos(t), sin(t)
        ex2 = rx * ct
        ey2 = ry * st
        f = -rx * st * (ex2 - lx) + ry * ct * (ey2 - ly)
        fp = (-rx * ct * (ex2 - lx) + rx * rx * st * st
              - ry * st * (ey2 - ly) + ry * ry * ct * ct)
        if abs(fp) < 1e-12:
            break
        delta = f / fp
        t -= delta
        if abs(delta) < 1e-9:
            break
    ct, st = cos(t), sin(t)
    return cx + rx * ct, cy + ry * st

# ======================================== ROUNDED RECT ========================================
def closest_pt_on_rr(px: float, py: float, cx: float, cy: float, hx: float, hy: float, r: float, rotation: float) -> tuple[float, float]:
    """Point le plus proche sur le contour du ``RoundedRect``"""
    rad = radians(-rotation)
    cos_r, sin_r = cos(rad), sin(rad)
    dx, dy = px - cx, py - cy
    lx =  dx * cos_r - dy * sin_r
    ly =  dx * sin_r + dy * cos_r

    clamp_x = max(-hx, min(hx, lx))
    clamp_y = max(-hy, min(hy, ly))

    ddx = lx - clamp_x
    ddy = ly - clamp_y
    dist = sqrt(ddx * ddx + ddy * ddy)

    if dist < 1e-10:
        dx_edge = hx - abs(lx)
        dy_edge = hy - abs(ly)
        if dx_edge < dy_edge:
            local_sx = (hx + r) * (1.0 if lx >= 0 else -1.0)
            local_sy = ly
        else:
            local_sx = lx
            local_sy = (hy + r) * (1.0 if ly >= 0 else -1.0)
    else:
        local_sx = clamp_x + ddx / dist * r
        local_sy = clamp_y + ddy / dist * r

    rad_w = radians(rotation)
    cos_w, sin_w = cos(rad_w), sin(rad_w)
    return (cx + local_sx * cos_w - local_sy * sin_w, cy + local_sx * sin_w + local_sy * cos_w,)

def depth_and_normal_rr(px: float, py: float, cx: float, cy: float, hx: float, hy: float, r: float, rotation: float) -> tuple[float, float, float] | None:
    """Penetration *depth* + *normale* pour un point ``(px,py)`` contre un ``RoundedRect``"""
    rad = radians(-rotation)
    cos_r, sin_r = cos(rad), sin(rad)
    dx, dy = px - cx, py - cy
    lx =  dx * cos_r - dy * sin_r
    ly =  dx * sin_r + dy * cos_r

    clamp_x = max(-hx, min(hx, lx))
    clamp_y = max(-hy, min(hy, ly))
    ddx = lx - clamp_x
    ddy = ly - clamp_y
    dist = sqrt(ddx * ddx + ddy * ddy)

    if dist > r:
        return None

    # Normale locale
    if dist < 1e-10:
        dx_edge = hx - abs(lx)
        dy_edge = hy - abs(ly)
        if dx_edge < dy_edge:
            nlx = 1.0 if lx >= 0 else -1.0
            nly = 0.0
            depth = r + dx_edge
        else:
            nlx = 0.0
            nly = 1.0 if ly >= 0 else -1.0
            depth = r + dy_edge
    else:
        nlx = ddx / dist
        nly = ddy / dist
        depth = r - dist

    # Retour en world
    rad_w = radians(rotation)
    cos_w, sin_w = cos(rad_w), sin(rad_w)
    nx = nlx * cos_w - nly * sin_w
    ny = nlx * sin_w + nly * cos_w
    return nx, ny, depth

# ======================================== EXPORTS ========================================
__all__ = [
    "closest_pt_on_seg",
    "closest_pt_seg_to_seg",
    "point_in_convex_poly",
    "to_ellipse_local",
    "from_ellipse_local",
    "closest_pt_on_ellipse",
    "closest_pt_on_rr",
    "depth_and_normal_rr",
]