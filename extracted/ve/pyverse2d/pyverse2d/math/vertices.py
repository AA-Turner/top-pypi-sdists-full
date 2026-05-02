# ======================================== IMPORTS ========================================
from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

# ======================================== VERIFICATION ========================================
def is_convex(vertices: NDArray[np.float32]) -> bool:
    """Vérifie que la forme soit convexe

    Args:
        vertices: ``(N, 2)`` points du polygone
    """
    v = np.asarray(vertices, dtype=np.float32)
    n = len(v)
    if n < 3:
        return False

    a = v
    b = np.roll(v, -1, axis=0)
    c = np.roll(v, -2, axis=0)

    cross = (b[:,0]-a[:,0]) * (c[:,1]-a[:,1]) - (b[:,1]-a[:,1]) * (c[:,0]-a[:,0])

    non_zero = cross[np.abs(cross) > 1e-8]
    if len(non_zero) == 0:
        return True

    return np.all(non_zero > 0) or np.all(non_zero < 0)

# ======================================== TRANSFORMATION ========================================
def center_vertices(vertices: NDArray[np.float32]) -> NDArray[np.float32]:
    """Recentre des vertices autour de ``(0, 0)``

    Args:
        vertices: ``(N, 2)`` points du polygone
    """
    v = np.asarray(vertices, dtype=np.float32)
    if len(v) == 0:
        return v

    center = v.mean(axis=0)
    return v - center


def center_bbox(vertices: NDArray[np.float32]) -> NDArray[np.float32]:
    """Recentre des vertices sur le milieu de leur bounding box

    Args:
        vertices: ``(N, 2)`` points du polygone
    """
    v = np.asarray(vertices, dtype=np.float32)
    if len(v) == 0:
        return v

    center = (v.min(axis=0) + v.max(axis=0)) / 2.0
    return v - center


def order_ccw(vertices: NDArray[np.float32]) -> NDArray[np.float32]:
    """Ordonne des vertices en sens anti-horaire (CCW)

    Args:
        vertices: ``(N, 2)`` points du polygone
    """
    v = np.asarray(vertices, dtype=np.float32)
    if len(v) < 3:
        return v

    # centre du polygone
    center = v.mean(axis=0)

    # angle polaire autour du centre
    angles = np.arctan2(v[:, 1] - center[1], v[:, 0] - center[0])

    order = np.argsort(angles)
    return v[order]

# ======================================== TRIANGULATION ========================================
def triangulate_triangle_fan(vertices: NDArray[np.float32]) -> NDArray[np.int32]:
    """Renvoie les indices des triangles d'un mesh

    Ne fonctionne qu'avec les formes convexes.

    Args:
        vertices: array ordonnée CCW (N, 2)
    """
    v = np.asarray(vertices, dtype=np.float32)

    n = len(v)
    if n < 3:
        return np.empty((0,), dtype=np.int32)

    # triangle fan : (0, i, i+1)
    idx = np.empty((n - 2) * 3, dtype=np.int32)

    k = 0
    for i in range(1, n - 1):
        idx[k] = 0
        idx[k + 1] = i
        idx[k + 2] = i + 1
        k += 3

    return idx


def triangulate_ear_clipping(vertices: NDArray[np.float32]) -> NDArray[np.int32]:
    """Renvoie les indices des triangles d'un mesh

    Ne fonctionne qu'avec les formes non autosécantes.

    Args:
        vertices: array ordonnée CCW (N, 2)
    """
    n = len(vertices)
    if n < 3:
        return np.empty((0,), dtype=np.int32)

    # Cas triangle trivial
    if n == 3:
        return np.array([0, 1, 2], dtype=np.int32)

    def cross(o, a, b) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def is_ear(i0, i1, i2) -> bool:
        a, b, c = vertices[i0], vertices[i1], vertices[i2]

        # doit être convexe (CCW)
        if cross(a, b, c) <= 0:
            return False

        # aucun autre point dans le triangle
        for j in range(n):
            if j in (i0, i1, i2):
                continue
            p = vertices[j]

            # barycentric / orientation test (point in triangle)
            c1 = cross(a, b, p)
            c2 = cross(b, c, p)
            c3 = cross(c, a, p)

            if c1 >= 0 and c2 >= 0 and c3 >= 0:
                return False

        return True

    # indices actifs
    idx = list(range(n))
    triangles = []

    guard = 0

    while len(idx) > 3 and guard < 10_000:
        guard += 1
        ear_found = False

        for i in range(len(idx)):
            i0 = idx[i - 1]
            i1 = idx[i]
            i2 = idx[(i + 1) % len(idx)]

            if is_ear(i0, i1, i2):
                triangles.extend([i0, i1, i2])
                del idx[i]
                ear_found = True
                break

        if not ear_found:
            # polygon probablement dégénéré
            break

    # dernier triangle restant
    if len(idx) == 3:
        triangles.extend([idx[0], idx[1], idx[2]])

    return np.array(triangles, dtype=np.int32)

# ======================================== EXPORTS ========================================
__all__ = [
    "is_convex",

    "center_vertices",
    "center_bbox",
    "order_ccw",

    "triangulate_triangle_fan",
    "triangulate_ear_clipping",
]