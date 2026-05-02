# ======================================== IMPORTS ========================================
from __future__ import annotations

from .....math import Vector
from .....abc import Shape
from .....shape import Ellipse, Capsule

from .._registry import Contact, register

from ._prim_transform import ellipse_params, capsule_params
from ._helper import closest_pt_on_seg, closest_pt_on_ellipse

from math import sqrt, cos, sin, atan2, pi as _PI

# ======================================== Ellipse × Ellipse ========================================
@register(Ellipse, Ellipse)
def ellipse_ellipse(sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float, sb: Shape, bx: float, by: float, scale_b: float, rot_b: float):
    ex_a, ey_a, rx_a, ry_a, rot_a_rad = ellipse_params(sa, ax, ay, scale_a, rot_a)
    ex_b, ey_b, rx_b, ry_b, rot_b_rad = ellipse_params(sb, bx, by, scale_b, rot_b)

    # Centre de B dans le repère local de A
    cos_r, sin_r = cos(-rot_a_rad), sin(-rot_a_rad)
    dx, dy = ex_b - ex_a, ey_b - ey_a
    cdx = dx * cos_r - dy * sin_r
    cdy = dx * sin_r + dy * cos_r

    # Rotation de B relative à A
    rel = rot_b_rad - rot_a_rad
    cos_rel, sin_rel = cos(rel), sin(rel)

    if cdx == 0.0 and cdy == 0.0:
        return Contact(Vector._make(1.0, 0.0), rx_a + rx_b)

    # Recherche grossière de l'axe de moindre pénétration
    _STEP = _PI / 24
    best_ov = float("inf")
    best_theta = atan2(cdy, cdx) % _PI

    for i in range(24):
        theta = i * _STEP
        ct, st = cos(theta), sin(theta)
        h_a = sqrt(rx_a * rx_a * ct * ct + ry_a * ry_a * st * st)
        
        # Axe theta dans le repère de B
        bt = ct * cos_rel + st * sin_rel
        bst = -ct * sin_rel + st * cos_rel
        h_b = sqrt(rx_b * rx_b * bt * bt + ry_b * ry_b * bst * bst)
        ov = h_a + h_b - abs(cdx * ct + cdy * st)
        if ov < best_ov:
            best_ov = ov
            best_theta = theta

    if best_ov <= 0:
        return None

    # Raffinement Newton
    theta = best_theta
    for _ in range(10):
        ct, st = cos(theta), sin(theta)

        h_a = sqrt(rx_a * rx_a * ct * ct + ry_a * ry_a * st * st) or 1e-10
        bt = ct * cos_rel + st * sin_rel
        bst = -ct * sin_rel + st * cos_rel
        h_b = sqrt(rx_b * rx_b * bt * bt + ry_b * ry_b * bst * bst) or 1e-10

        c_proj = cdx * ct + cdy * st
        sign_c = 1.0 if c_proj >= 0.0 else -1.0

        # Premières dérivées par rapport à theta
        h_a_p = ((ry_a * ry_a - rx_a * rx_a) * st * ct) / h_a

        bt_p = -st * cos_rel + ct * sin_rel
        bst_p = st * sin_rel + ct * cos_rel
        h_b_p = (rx_b * rx_b * bt * bt_p + ry_b * ry_b * bst * bst_p) / h_b

        c_p = -cdx * st + cdy * ct

        ov_p = h_a_p + h_b_p - sign_c * c_p

        # Secondes dérivées par rapport à theta
        cos2t = ct * ct - st * st
        h_a_pp = ((ry_a * ry_a - rx_a * rx_a) * cos2t) / h_a - (h_a_p * h_a_p) / h_a

        bt_pp = -ct * cos_rel - st * sin_rel
        bst_pp = -ct * sin_rel + st * cos_rel
        h_b_pp = (
            rx_b * rx_b * (bt_pp * bt + bt_p * bt_p) +
            ry_b * ry_b * (bst_pp * bst + bst_p * bst_p)
        ) / h_b - (h_b_p * h_b_p) / h_b

        ov_pp = h_a_pp + h_b_pp + abs(c_proj)

        if abs(ov_pp) < 1e-12:
            break
        delta = ov_p / ov_pp
        theta -= delta
        if abs(delta) < 1e-8:
            break

    ct, st = cos(theta), sin(theta)
    h_a = sqrt(rx_a * rx_a * ct * ct + ry_a * ry_a * st * st)
    bt = ct * cos_rel + st * sin_rel
    bst = -ct * sin_rel + st * cos_rel
    h_b = sqrt(rx_b * rx_b * bt * bt + ry_b * ry_b * bst * bst)
    c_proj = cdx * ct + cdy * st
    overlap = h_a + h_b - abs(c_proj)

    if overlap <= 0:
        return None

    # Normale en local A → world
    sign_c = 1.0 if c_proj >= 0.0 else -1.0
    nlx, nly = -ct * sign_c, -st * sign_c
    cos_w, sin_w = cos(rot_a_rad), sin(rot_a_rad)
    return Contact(Vector._make(
        nlx * cos_w - nly * sin_w,
        nlx * sin_w + nly * cos_w,
    ), overlap)

# ======================================== Ellipse × Capsule ========================================
@register(Ellipse, Capsule)
def ellipse_capsule(sa: Shape, ax: float, ay: float, scale_a: float, rot_a: float, sb: Shape, bx: float, by: float, scale_b: float, rot_b: float):
    """Vérifie la collision entre ``Ellipse`` et ``Capsule``"""
    ex, ey, rx, ry, rot_rad = ellipse_params(sa, ax, ay, scale_a, rot_a)
    cap_ax, cap_ay, cap_bx, cap_by, cap_r = capsule_params(sb, bx, by, scale_b, rot_b)
    spine_dx, spine_dy = cap_bx - cap_ax, cap_by - cap_ay
    qx, qy = closest_pt_on_seg(cap_ax, cap_ay, spine_dx, spine_dy, ex, ey)
    cos_r, sin_r = cos(-rot_rad), sin(-rot_rad)
    dx, dy = qx - ex, qy - ey
    qlx = dx * cos_r - dy * sin_r
    qly = dx * sin_r + dy * cos_r
    inside = (qlx / rx) ** 2 + (qly / ry) ** 2 <= 1.0
    cpx_l, cpy_l = closest_pt_on_ellipse(0.0, 0.0, rx, ry, qlx, qly)
    ddx, ddy = qlx - cpx_l, qly - cpy_l
    dist = sqrt(ddx * ddx + ddy * ddy) or 1e-8
    cos_w, sin_w = cos(rot_rad), sin(rot_rad)
    nx = -(ddx / dist) * cos_w + (ddy / dist) * sin_w
    ny = -(ddx / dist) * sin_w - (ddy / dist) * cos_w
    if inside:
        return Contact(Vector._make(nx, ny), cap_r + dist)
    if dist >= cap_r:
        return None
    return Contact(Vector._make(nx, ny), cap_r - dist)

# ======================================== EXPORTS ========================================
__all__ = [
    "ellipse_ellipse",
    "ellipse_capsule",
]