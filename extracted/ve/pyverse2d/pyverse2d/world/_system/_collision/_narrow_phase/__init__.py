# ======================================== IMPORTS ========================================
from __future__ import annotations

from ....._core import Geometry
from .....abc import Shape

from .._registry import _handlers, Contact

from ._vertex import sat, circle_vs_pts, ellipse_vs_pts, capsule_vs_pts

from . import _circle, _ellipse, _capsule, _rounded_rect     # noqa: F401 (enregistrement des handlers)
from ._prim_transform import circle_params, ellipse_params, capsule_params

import numpy as np
from numpy.typing import NDArray

# ======================================== DISPATCH ========================================
def dispatch(geom_a: Geometry, geom_b: Geometry) -> Contact | None:
    """Fait correspondre les shapes à leur test de collision
    
    Args:
        geom_a: géométrie de la forme A
        geom_b: géométrie de la forme B
    """
    # Forme A
    sa = geom_a.shape
    tr_a = geom_a.transform
    ax, ay = geom_a.world_center()
    scale_a = tr_a.scale
    rot_a = tr_a.rotation

    # Forme B
    sb = geom_b.shape
    tr_b = geom_b.transform
    bx, by = geom_b.world_center()
    scale_b = tr_b.scale
    rot_b = tr_b.rotation

    # Vérifications si primitives
    a_is_prim = sa.is_primitive()
    b_is_prim = sb.is_primitive()

    # Primitive vs Primitive
    if a_is_prim and b_is_prim:
        # A vs B
        key = (type(sa), type(sb))
        fn = _handlers.get(key)
        if fn:
            return fn(sa, ax, ay, scale_a, rot_a, sb, bx, by, scale_b, rot_b)
        
        # B vs A
        key_flip = (type(sb), type(sa))
        fn = _handlers.get(key_flip)
        if fn:
            c = fn(sb, bx, by, scale_b, rot_b, sa, ax, ay, scale_a, rot_a)
            return _flip(c)
        
        # Cas non supporté
        return None

    # Primitive vs Vertex
    if a_is_prim and not b_is_prim:
        pts_b = geom_b.world_vertices()
        c = _primitive_vs_pts(sa, ax, ay, scale_a, rot_a, pts_b)
        return c

    # Vertex vs Primitive
    if not a_is_prim and b_is_prim:
        pts_a = geom_a.world_vertices()
        c = _primitive_vs_pts(sb, bx, by, scale_b, rot_b, pts_a)
        return _flip(c)

    # Vertex vs Vertex
    pts_a = geom_a.world_vertices()
    pts_b = geom_b.world_vertices()
    return sat(pts_a, pts_b)

# ======================================== HELPERS ========================================
def _primitive_vs_pts(
    sp: Shape,
    px: float,
    py: float,
    scale_p: float,
    rot_p: float,
    pts: NDArray[np.float32]
) -> Contact | None:
    """Dispatch une primitive contre un contour polygonal
    
    Args:
        sp: forme de la ``PrimitiveShape``
        px: position horizontale de la ``PrimitiveShape``
        py: position verticale de la ``PrimitiveShape``
        scale_p: facteur de redimensionnement de la ``PrimitiveShape``
        rot_p: angle de rotation de la ``PrimitiveShape``
        pts: points du polygone
    """
    _idp = sp.id()

    if _idp == "circle":
        cx, cy, r = circle_params(sp, px, py, scale_p)
        return circle_vs_pts(cx, cy, r, pts)

    if _idp == "ellipse":
        cx, cy, rx, ry, r = ellipse_params(sp, px, py, scale_p, rot_p)
        return ellipse_vs_pts(cx, cy, rx, ry, r, pts)

    if _idp == "capsule":
        ax_, ay_, bx_, by_, r = capsule_params(sp, px, py, scale_p, rot_p)
        return capsule_vs_pts(ax_, ay_, bx_, by_, r, pts)

    return None

def _flip(c: Contact | None) -> Contact | None:
    """Inverse le sens d'un contact
    
    Args:
        c: ``Contact`` à inverser
    """
    if c is None:
        return None
    c.normal = -c.normal
    return c

# ======================================== EXPORTS ========================================
__all__ = [
    "dispatch",
]