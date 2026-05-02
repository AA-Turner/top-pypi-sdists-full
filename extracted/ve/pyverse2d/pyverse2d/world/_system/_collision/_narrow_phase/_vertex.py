# ======================================== IMPORTS ========================================
from __future__ import annotations

from .....math import Vector

from .._registry import Contact

from ._helper import closest_pt_on_seg, closest_pt_seg_to_seg, point_in_convex_poly

from math import sqrt, cos, sin
import numpy as np
from numpy.typing import NDArray

# ======================================== SAT ========================================
def sat(pts_a: NDArray[np.float32], pts_b: NDArray[np.float32]) -> Contact | None:
    """SAT vectorisé pour deux polygones convexes"""
    min_depth = float("inf")
    best_nx, best_ny = 0.0, 1.0

    for pts, other in ((pts_a, pts_b), (pts_b, pts_a)):
        edges = np.roll(pts, -1, axis=0) - pts
        lengths = np.linalg.norm(edges, axis=1, keepdims=True)
        mask = lengths[:, 0] > 1e-10
        normals = np.where(np.repeat(mask[:, np.newaxis], 2, axis=1), np.stack([-edges[:, 1], edges[:, 0]], axis=1) / np.where(lengths > 1e-10, lengths, 1.0), 0.0)

        for i in range(len(pts)):
            if not mask[i]:
                continue
            nx, ny = float(normals[i, 0]), float(normals[i, 1])
            proj_a = pts   @ np.array([nx, ny], dtype=np.float32)
            proj_b = other @ np.array([nx, ny], dtype=np.float32)
            min_a, max_a = float(proj_a.min()), float(proj_a.max())
            min_b, max_b = float(proj_b.min()), float(proj_b.max())
            ov = min(max_a, max_b) - max(min_a, min_b)
            if ov <= 0:
                return None
            if ov < min_depth:
                min_depth = ov
                best_nx, best_ny = nx, ny

    ca = pts_a.mean(axis=0)
    cb = pts_b.mean(axis=0)
    if float((ca[0] - cb[0]) * best_nx + (ca[1] - cb[1]) * best_ny) < 0:
        best_nx, best_ny = -best_nx, -best_ny

    return Contact(Vector._make(best_nx, best_ny), min_depth)

# ======================================== CIRCLE VS POLYGONE ========================================
def circle_vs_pts(cx: float, cy: float, cr: float, pts: NDArray[np.float32]) -> Contact | None:
    """Cercle vs polygone convexe"""
    n = len(pts)
    min_depth = float("inf")
    best_nx, best_ny = 0.0, 1.0

    mean = pts.mean(axis=0)
    pg_cx, pg_cy = float(mean[0]), float(mean[1])

    edges = np.roll(pts, -1, axis=0) - pts
    lengths = np.linalg.norm(edges, axis=1)

    for i in range(n):
        le = float(lengths[i])
        if le < 1e-10:
            continue
        nx = float(-edges[i, 1]) / le
        ny = float( edges[i, 0]) / le
        nv = np.array([nx, ny], dtype=np.float32)
        proj = pts @ nv
        min_p, max_p = float(proj.min()), float(proj.max())
        pc = cx * nx + cy * ny
        ov = min(pc + cr, max_p) - max(pc - cr, min_p)
        if ov <= 0:
            return None
        if ov < min_depth:
            min_depth = ov
            best_nx, best_ny = nx, ny

    diffs = pts - np.array([cx, cy], dtype=np.float32)
    dists_sq = (diffs ** 2).sum(axis=1)
    nearest = int(dists_sq.argmin())
    ddx = cx - float(pts[nearest, 0])
    ddy = cy - float(pts[nearest, 1])
    le = sqrt(ddx * ddx + ddy * ddy) or 1e-8
    nx, ny = ddx / le, ddy / le
    nv = np.array([nx, ny], dtype=np.float32)
    proj = pts @ nv
    min_p, max_p = float(proj.min()), float(proj.max())
    pc = cx * nx + cy * ny
    ov = min(pc + cr, max_p) - max(pc - cr, min_p)
    if ov <= 0:
        return None
    if ov < min_depth:
        min_depth = ov
        best_nx, best_ny = nx, ny

    if best_nx * (cx - pg_cx) + best_ny * (cy - pg_cy) < 0:
        best_nx, best_ny = -best_nx, -best_ny

    return Contact(Vector._make(best_nx, best_ny), min_depth)

# ======================================== ELLIPSE VS POLYGONE ========================================
def ellipse_vs_pts(ex: float, ey: float, rx: float, ry: float, rot_rad: float, pts: NDArray[np.float32]) -> Contact | None:
    """Ellipse vs polygone convexe"""
    cos_r, sin_r = cos(-rot_rad), sin(-rot_rad)
    shifted = pts - np.array([ex, ey], dtype=np.float32)
    local_pts = np.stack([
        shifted[:, 0] * cos_r - shifted[:, 1] * sin_r,
        shifted[:, 0] * sin_r + shifted[:, 1] * cos_r,
    ], axis=1)

    n = len(local_pts)
    center = local_pts.mean(axis=0)
    pg_cx, pg_cy = float(center[0]), float(center[1])
    min_ov = float("inf")
    best_nlx, best_nly = 0.0, 1.0 

    def _test_axis(nx: float, ny: float) -> bool:
        nonlocal min_ov, best_nlx, best_nly
        le = sqrt(nx * nx + ny * ny)
        if le < 1e-10:
            return True
        nx /= le
        ny /= le
        h = sqrt(rx * rx * nx * nx + ry * ry * ny * ny)
        nv = np.array([nx, ny], dtype=np.float32)
        projs = local_pts @ nv
        min_p, max_p = float(projs.min()), float(projs.max())
        ov = min(h, max_p) - max(-h, min_p)
        if ov <= 0:
            return False
        if ov < min_ov:
            min_ov = ov
            mid = (min_p + max_p) * 0.5
            if abs(mid) > 1e-6:
                best_nlx, best_nly = (nx, ny) if mid < 0 else (-nx, -ny)
            else:
                best_nlx, best_nly = (nx, ny) if -pg_cx * nx - pg_cy * ny > 0 else (-nx, -ny)
        return True

    edges = np.roll(local_pts, -1, axis=0) - local_pts
    for i in range(n):
        if not _test_axis(float(-edges[i, 1]), float(edges[i, 0])):
            return None

    min_d2 = float("inf")
    cpx, cpy = float(local_pts[0, 0]), float(local_pts[0, 1])
    for i in range(n):
        x1, y1 = float(local_pts[i, 0]), float(local_pts[i, 1])
        x2, y2 = float(local_pts[(i + 1) % n, 0]), float(local_pts[(i + 1) % n, 1])
        px_, py_ = closest_pt_on_seg(x1, y1, x2 - x1, y2 - y1, 0.0, 0.0)
        d2 = px_ ** 2 + py_ ** 2
        if d2 < min_d2:
            min_d2 = d2
            cpx, cpy = px_, py_
    if not _test_axis(cpx, cpy):
        return None

    cos_w, sin_w = cos(rot_rad), sin(rot_rad)
    best_nx = best_nlx * cos_w - best_nly * sin_w
    best_ny = best_nlx * sin_w + best_nly * cos_w
    return Contact(Vector._make(best_nx, best_ny), min_ov)

# ======================================== CAPSULE VS POLYGONE ========================================
def capsule_vs_pts(ax: float, ay: float, bx: float, by: float, r: float, pts: NDArray[np.float32]) -> Contact | None:
    """Capsule vs polygone convexe"""
    n = len(pts)
    spine_dx = bx - ax
    spine_dy = by - ay
    mid_x = ax + spine_dx * 0.5
    mid_y = ay + spine_dy * 0.5
    min_dist = float("inf")
    best_nx, best_ny = 0.0, 1.0

    for i in range(n):
        px1, py1 = float(pts[i, 0]), float(pts[i, 1])
        px2, py2 = float(pts[(i + 1) % n, 0]), float(pts[(i + 1) % n, 1])
        edx = px2 - px1
        edy = py2 - py1
        le = sqrt(edx * edx + edy * edy)
        if le < 1e-10:
            continue
        enx, eny = -edy / le, edx / le
        sp_x, sp_y = closest_pt_seg_to_seg(ax, ay, spine_dx, spine_dy, px1, py1, edx, edy)
        ep_x, ep_y = closest_pt_on_seg(px1, py1, edx, edy, sp_x, sp_y)
        ddx = sp_x - ep_x
        ddy = sp_y - ep_y
        dist = sqrt(ddx * ddx + ddy * ddy)
        if dist < min_dist:
            min_dist = dist
            if dist > 1e-8:
                best_nx, best_ny = ddx / dist, ddy / dist
            else:
                best_nx, best_ny = enx, eny

    if min_dist > 1e-6 and point_in_convex_poly(mid_x, mid_y, pts):
        near_dist = float("inf")
        near_nx, near_ny = 0.0, 1.0
        for i in range(n):
            px1, py1 = float(pts[i, 0]), float(pts[i, 1])
            px2, py2 = float(pts[(i + 1) % n, 0]), float(pts[(i + 1) % n, 1])
            edx = px2 - px1
            edy = py2 - py1
            le = sqrt(edx * edx + edy * edy)
            if le < 1e-10:
                continue
            ep_x, ep_y = closest_pt_on_seg(px1, py1, edx, edy, mid_x, mid_y)
            ddx = mid_x - ep_x
            ddy = mid_y - ep_y
            d = sqrt(ddx * ddx + ddy * ddy)
            if d < near_dist:
                near_dist = d
                if d > 1e-8:
                    near_nx, near_ny = ddx / d, ddy / d
                else:
                    near_nx, near_ny = -edy / le, edx / le
        return Contact(Vector._make(near_nx, near_ny), r + near_dist)

    if min_dist >= r:
        return None

    poly_cx = float(pts.mean(axis=0)[0])
    poly_cy = float(pts.mean(axis=0)[1])
    if best_nx * (mid_x - poly_cx) + best_ny * (mid_y - poly_cy) < 0:
        best_nx, best_ny = -best_nx, -best_ny

    return Contact(Vector._make(best_nx, best_ny), r - min_dist)