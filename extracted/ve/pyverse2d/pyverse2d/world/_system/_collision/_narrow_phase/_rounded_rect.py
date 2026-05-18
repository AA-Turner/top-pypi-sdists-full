# ======================================== IMPORTS ========================================
from __future__ import annotations

from .....math import Vector
from .....abc import Shape
from .....shape import Circle, Ellipse, Capsule, RoundedRect

from .._registry import Contact, register

from ._prim_transform import circle_params, ellipse_params, capsule_params, rounded_rect_params
from ._helper import closest_pt_on_seg, closest_pt_on_ellipse, depth_and_normal_rr, closest_pt_on_rr

from math import sqrt, cos, sin

# ======================================== RoundedRect × RoundedRect ========================================
@register(RoundedRect, RoundedRect)
def rr_rr(
    sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float,
    sb: Shape, bx: float, by: float, scale_b: float, rot_b: float,
) -> Contact | None:
    """Vérifie la collision entre ``RoundedRect`` et ``RoundedRect``
    
    Args:
        sa: forme ``A``
        ax: centre horizontal ``A``
        ay: centre vertical ``A``
        scale_a: facteur de redimensionnement ``A``
        rot_a: angle de rotation ``A``
        sb: forme ``B``
        bx: centre horizontal ``B``
        by: centre vertical ``B``
        scale_b: facteur de redimensionnement ``B``
        rot_b: angle de rotation `B``
    """
    # Récupération des paramètres
    cx_a, cy_a, hx_a, hy_a, r_a, rot_a, _ = rounded_rect_params(sa, ax, ay, scale_a, rot_a)
    cx_b, cy_b, hx_b, hy_b, r_b, rot_b, _ = rounded_rect_params(sb, bx, by, scale_b, rot_b)

    # Calcul des pénétrations
    result_a = depth_and_normal_rr(cx_a, cy_a, cx_b, cy_b, hx_b, hy_b, r_b + r_a, rot_b)
    result_b = depth_and_normal_rr(cx_b, cy_b, cx_a, cy_a, hx_a, hy_a, r_a + r_b, rot_a)

    # Vérification de la collision
    if result_a is None and result_b is None:
        return None
    if result_a is None:
        nx, ny, depth = result_b
        return Contact(Vector._make(-nx, -ny), depth)
    if result_b is None:
        nx, ny, depth = result_a
        return Contact(Vector._make(nx, ny), depth)
    if result_a[2] <= result_b[2]:
        nx, ny, depth = result_a
        return Contact(Vector._make(nx, ny), depth)
    nx, ny, depth = result_b
    return Contact(Vector._make(-nx, -ny), depth)

# ======================================== RoundedRect × Circle ========================================
@register(RoundedRect, Circle)
def rr_circle(
    sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float,
    sb: Shape, bx: float, by: float, scale_b: float, rot_b: float,
) -> Contact | None:
    """Vérifie la collision entre ``RoundedRect`` et ``Circle``
    
    Args:
        sa: forme ``A``
        ax: centre horizontal ``A``
        ay: centre vertical ``A``
        scale_a: facteur de redimensionnement ``A``
        rot_a: angle de rotation ``A``
        sb: forme ``B``
        bx: centre horizontal ``B``
        by: centre vertical ``B``
        scale_b: facteur de redimensionnement ``B``
        rot_b: angle de rotation `B``
    """
    # Récupération des paramètre
    cx, cy, hx, hy, r, rot, _ = rounded_rect_params(sa, ax, ay, scale_a, rot_a)
    _, _, rb = circle_params(sb, bx, by, scale_b)

    # Calcul de la pénétration
    result = depth_and_normal_rr(bx, by, cx, cy, hx, hy, r + rb, rot)

    # Vérification de la collision
    if result is None:
        return None
    nx, ny, depth = result
    return Contact(Vector._make(-nx, -ny), depth)

# ======================================== RoundedRect × Ellipse ========================================
@register(RoundedRect, Ellipse)
def rr_ellipse(
    sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float,
    sb: Shape, bx: float, by: float, scale_b: float, rot_b: float,
) -> Contact | None:
    """Vérifie la collision entre ``RoundedRect`` et ``Ellipse``
    
    Args:
        sa: forme ``A``
        ax: centre horizontal ``A``
        ay: centre vertical ``A``
        scale_a: facteur de redimensionnement ``A``
        rot_a: angle de rotation ``A``
        sb: forme ``B``
        bx: centre horizontal ``B``
        by: centre vertical ``B``
        scale_b: facteur de redimensionnement ``B``
        rot_b: angle de rotation `B``
    """
    # Récupération des paramètres
    cx, cy, hx, hy, r, rot, _ = rounded_rect_params(sa, ax, ay, scale_a, rot_a)
    ex, ey, rx, ry, rot_rad = ellipse_params(sb, bx, by, scale_b, rot_b)

    # Calcul du point le plus proche
    qx, qy = closest_pt_on_rr(ex, ey, cx, cy, hx, hy, r, rot)

    # Passage dans le repère local de l'ellipse
    cos_r, sin_r = cos(-rot_rad), sin(-rot_rad)
    dx, dy = qx - ex, qy - ey
    qlx = dx * cos_r - dy * sin_r
    qly = dx * sin_r + dy * cos_r

    # Calcul  du chevauchement
    inside = (qlx / rx) ** 2 + (qly / ry) ** 2 <= 1.0
    cpx_l, cpy_l = closest_pt_on_ellipse(0.0, 0.0, rx, ry, qlx, qly)
    ddx, ddy = qlx - cpx_l, qly - cpy_l
    dist = sqrt(ddx * ddx + ddy * ddy) or 1e-8

    # Vérification de la collision
    if not inside and dist >= 1e-6:
        return None
    
    # Passage local vers monde
    cos_w, sin_w = cos(rot_rad), sin(rot_rad)
    nx = (ddx / dist) * cos_w - (ddy / dist) * sin_w
    ny = (ddx / dist) * sin_w + (ddy / dist) * cos_w
    return Contact(Vector._make(-nx, -ny), dist)

# ======================================== RoundedRect × Capsule ========================================
@register(RoundedRect, Capsule)
def rr_capsule(
    sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float,
    sb: Shape, bx: float, by: float, scale_b: float, rot_b: float,
) -> Contact | None:
    """Vérifie la collision entre ``RoundedRect`` et ``Capsule``
    
    Args:
        sa: forme ``A``
        ax: centre horizontal ``A``
        ay: centre vertical ``A``
        scale_a: facteur de redimensionnement ``A``
        rot_a: angle de rotation ``A``
        sb: forme ``B``
        bx: centre horizontal ``B``
        by: centre vertical ``B``
        scale_b: facteur de redimensionnement ``B``
        rot_b: angle de rotation `B``
    """
    # Récupération des paramètres
    cx, cy, hx, hy, r, rot, _ = rounded_rect_params(sa, ax, ay, scale_a, rot_a)
    cap_ax, cap_ay, cap_bx, cap_by, cap_r = capsule_params(sb, bx, by, scale_b, rot_b)

    # Calcul des distances
    spine_dx, spine_dy = cap_bx - cap_ax, cap_by - cap_ay
    qx, qy = closest_pt_on_seg(cap_ax, cap_ay, spine_dx, spine_dy, cx, cy)
    result = depth_and_normal_rr(qx, qy, cx, cy, hx, hy, r + cap_r, rot)

    # Vérification de la collision
    if result is None:
        return None
    nx, ny, depth = result
    return Contact(Vector._make(-nx, -ny), depth)

# ======================================== EXPORTS ========================================
__all__ = [
    "rr_rr",
    "rr_circle",
    "rr_ellipse",
    "rr_capsule",
]