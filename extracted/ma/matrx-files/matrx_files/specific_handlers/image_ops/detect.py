"""Document boundary detection (OpenCV) — phone-scanner auto-crop.

``detect_document_quad(image_bytes)`` finds the outer boundary of a
photographed document (paper, receipt, card) and returns an ordered
quad suitable for the ``perspective_crop`` op.

Coordinate space: **post-EXIF-transpose pixels** — the orientation a
browser displays. The same space ``perspective_crop`` consumes, so the
FE can pass the returned quad straight back without conversion.

OpenCV is an optional backend (same posture as ``inpaint``): the module
imports cleanly without it and raises an actionable RuntimeError at
call time when missing.
"""

from __future__ import annotations

import io
from typing import Any

from PIL import Image, ImageOps

try:  # pragma: no cover - environment-dependent
    from pillow_heif import register_heif_opener  # type: ignore

    register_heif_opener()
except ImportError:  # pragma: no cover
    pass

# Downscale target for the detection pass — contours don't need full res,
# and Canny on a 12MP frame is pure waste. Returned coords are rescaled.
_DETECT_MAX_DIM = 1200

# A candidate quad must cover at least this fraction of the frame.
_MIN_AREA_RATIO = 0.20


def detect_document_quad(image_bytes: bytes, *, mode: str = "standard") -> dict[str, Any]:
    """Detect the dominant document quad in a photo.

    ``mode="standard"`` is the conservative Canny-contour pass (strict:
    convex 4-gon covering ≥20% of frame). ``mode="relaxed"`` is the
    "try again" pass for when standard finds nothing — brightness
    threshold (Otsu) + morphological close, eps sweep on the polygon
    approximation, lower area floor, and a min-area-rect fallback. It
    is markedly better on the common scanner case (light page on a dark
    surface) at the cost of occasionally grabbing a non-document bright
    region — which is why it is user-triggered, not the default.

    Returns::

        {
          "found": bool,
          "quad": {"top_left": [x, y], "top_right": …,
                   "bottom_right": …, "bottom_left": …} | None,
          "confidence": float,        # 0..1
          "image_width": int,         # post-EXIF-transpose dims
          "image_height": int,
        }
    """
    try:
        import cv2  # type: ignore
        import numpy as np
    except ImportError as e:  # pragma: no cover
        from matrx_files._extras import missing_extra_message

        raise RuntimeError(missing_extra_message("media", e.name or "cv2", "Document detection")) from e

    image = ImageOps.exif_transpose(Image.open(io.BytesIO(image_bytes)))
    if image.mode != "RGB":
        image = image.convert("RGB")
    full_w, full_h = image.size

    scale = min(1.0, _DETECT_MAX_DIM / max(full_w, full_h))
    if scale < 1.0:
        small = image.resize((round(full_w * scale), round(full_h * scale)), Image.BILINEAR)
    else:
        small = image
    frame = cv2.cvtColor(np.asarray(small), cv2.COLOR_RGB2GRAY)
    frame_area = frame.shape[0] * frame.shape[1]

    not_found = {
        "found": False,
        "quad": None,
        "confidence": 0.0,
        "image_width": full_w,
        "image_height": full_h,
    }

    if mode == "relaxed":
        result = _detect_relaxed(cv2, np, frame, frame_area)
    else:
        result = _detect_standard(cv2, np, frame, frame_area)
    if result is None:
        return not_found
    best_quad, best_area = result

    ordered = _order_corners(best_quad)
    confidence = _confidence(ordered, best_area / frame_area)

    # Rescale to full-resolution coordinates.
    inv = 1.0 / scale
    quad = {
        name: [round(float(x) * inv, 1), round(float(y) * inv, 1)]
        for name, (x, y) in zip(
            ("top_left", "top_right", "bottom_right", "bottom_left"), ordered
        )
    }
    return {
        "found": True,
        "quad": quad,
        "confidence": round(confidence, 3),
        "image_width": full_w,
        "image_height": full_h,
    }


def _detect_standard(cv2, np, frame, frame_area):
    """Conservative Canny-contour pass: convex 4-gon ≥20% of frame."""
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    # Median-based auto thresholds keep Canny stable across exposure levels.
    median = float(np.median(blurred))
    lower = int(max(0, 0.66 * median))
    upper = int(min(255, 1.33 * median))
    edges = cv2.Canny(blurred, lower, upper)
    edges = cv2.dilate(
        edges, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2
    )

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:10]:
        area = cv2.contourArea(contour)
        if area < _MIN_AREA_RATIO * frame_area:
            break  # sorted desc — everything after is smaller
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            return approx.reshape(4, 2).astype(np.float64), area
    return None


# Relaxed pass tunables.
_RELAXED_MIN_AREA_RATIO = 0.08
_RELAXED_EPS_SWEEP = (0.01, 0.02, 0.03, 0.05)


def _detect_relaxed(cv2, np, frame, frame_area):
    """Brightness-region pass for hard cases (light page, dark surface).

    Otsu threshold → morphological close → largest bright contour →
    eps-sweep 4-gon approximation, with a min-area-rect fallback so a
    plausible page region ALWAYS yields a quad.
    """
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    _, mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(contour)
    if area < _RELAXED_MIN_AREA_RATIO * frame_area:
        return None

    peri = cv2.arcLength(contour, True)
    hull = cv2.convexHull(contour)
    for eps in _RELAXED_EPS_SWEEP:
        approx = cv2.approxPolyDP(hull, eps * peri, True)
        if len(approx) == 4:
            return approx.reshape(4, 2).astype(np.float64), area
    # Fallback: tightest rotated rectangle around the bright region.
    box = cv2.boxPoints(cv2.minAreaRect(contour))
    return np.asarray(box, dtype=np.float64), area


def _order_corners(pts) -> list[tuple[float, float]]:
    """Order 4 points TL, TR, BR, BL via the sum/diff heuristic."""
    from matrx_files._extras import require

    np = require("numpy", "media", "Document detection")
    pts = np.asarray(pts, dtype=np.float64)
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1).ravel()  # y - x
    tl = pts[int(np.argmin(s))]
    br = pts[int(np.argmax(s))]
    tr = pts[int(np.argmin(d))]
    bl = pts[int(np.argmax(d))]
    return [tuple(tl), tuple(tr), tuple(br), tuple(bl)]


def _confidence(ordered: list[tuple[float, float]], area_ratio: float) -> float:
    """Blend of coverage and corner-angle sanity (right angles ≈ document)."""
    import math

    def _angle(a, b, c) -> float:
        """Interior angle at b, degrees."""
        v1 = (a[0] - b[0], a[1] - b[1])
        v2 = (c[0] - b[0], c[1] - b[1])
        n1 = math.hypot(*v1) or 1e-9
        n2 = math.hypot(*v2) or 1e-9
        cos = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
        return math.degrees(math.acos(cos))

    angles = [
        _angle(ordered[(i - 1) % 4], ordered[i], ordered[(i + 1) % 4]) for i in range(4)
    ]
    # 1.0 when all corners are 90°, decaying linearly to 0 at ±45° deviation.
    angle_score = max(0.0, 1.0 - max(abs(a - 90.0) for a in angles) / 45.0)
    coverage_score = min(1.0, area_ratio / 0.5)
    return max(0.0, min(1.0, 0.5 * coverage_score + 0.5 * angle_score))
