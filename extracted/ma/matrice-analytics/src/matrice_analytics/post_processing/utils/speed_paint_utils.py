"""Finding painted road markings in a still image of a road.

Split out of :mod:`speed_paint_calibration_utils` so each half stays inside the org
file-size cap, and because the two really are different jobs: this one turns pixels into
line segments, that one turns line segments into a camera.

THREE THINGS THAT HAVE TO BE RIGHT, AND ARE EASY TO GET WRONG
    1. A marking is not simply BRIGHT. Dry asphalt is unsaturated and sits well above 130
       in value, so an absolute brightness threshold selects the entire carriageway. What
       distinguishes paint is that it is brighter than the road IMMEDIATELY AROUND IT and
       thin -- a morphological top-hat, not a threshold.
    2. A road scene is dominated by lines running ALONG the road: lane edges, kerbs,
       barriers, the road edge itself. They converge on VP1, not VP2, and they outnumber
       the transverse markings. :func:`split_by_vp1` removes them explicitly, and returns
       them, because they are independent evidence about VP1.
    3. Shadows and sunlit foliage survive every colour test ever written. A road mask
       built from where vehicles have actually been seen does not care: a sunlit tree is
       thin, bright and unsaturated in places, but it is not a place cars drive.
"""

import math
from typing import List, Optional, Tuple

import cv2
import numpy as np


def paint_mask(
    background: np.ndarray,
    tophat: int = 35,
    tophat_thresh: int = 22,
    roi_top: float = 0.30,
    road: Optional[np.ndarray] = None,
) -> np.ndarray:
    """Thin, bright, white-or-yellow structure below the horizon.

    ``tophat`` must be wider than the widest marking and narrower than a lane: a kernel
    wider than a lane stops treating the lane as background, and the whole carriageway
    starts to respond.
    """
    height = background.shape[0]
    hsv = cv2.cvtColor(background, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (tophat, tophat))
    bright = cv2.morphologyEx(val, cv2.MORPH_TOPHAT, kernel) > tophat_thresh

    hi, si = hue.astype(int), sat.astype(int)
    white = si < 70
    yellow = (hi > 14) & (hi < 42) & (si > 60)

    mask = ((bright & (white | yellow)).astype(np.uint8)) * 255
    mask[: int(roi_top * height), :] = 0
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    if road is not None:
        mask = cv2.bitwise_and(mask, road)
    return mask


def road_mask_from_points(
    points: List[Tuple[float, float]],
    width: int,
    height: int,
    dilate: int = 25,
    box_px: int = 24,
) -> np.ndarray:
    """Where vehicles have been seen is road. Cheap, and better than any colour rule.

    A sunlit tree is thin, bright and unsaturated in places, so it survives every colour
    test ever written. What it is not is a place cars drive. ``points`` are the ground
    contact points of tracked vehicles, in pixels.
    """
    mask = np.zeros((height, width), np.uint8)
    half = max(1, box_px // 2)
    for x, y in points:
        cv2.rectangle(
            mask,
            (int(x) - half, int(y) - half),
            (int(x) + half, int(y) + half),
            255,
            -1,
        )
    if dilate > 1:
        mask = cv2.dilate(mask, np.ones((dilate, dilate), np.uint8))
    return mask


def segments_from_paint(mask: np.ndarray, min_len: int = 30, max_gap: int = 4) -> np.ndarray:
    """Straight segments along the edges of the painted regions."""
    edges = cv2.Canny(cv2.GaussianBlur(mask, (3, 3), 0), 40, 120)
    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        threshold=int(0.7 * min_len),
        minLineLength=min_len,
        maxLineGap=max_gap,
    )
    if lines is None:
        return np.zeros((0, 4))
    return lines.reshape(-1, 4).astype(float)


def split_by_vp1(
    segs: np.ndarray,
    vp1: np.ndarray,
    vp1_reject_deg: float = 12.0,
    vertical_reject_deg: float = 25.0,
) -> Tuple[np.ndarray, np.ndarray, int]:
    """Split paint segments into ``(transverse, along_road, n_vertical)``.

    The along-road family is RETURNED rather than discarded, because it is free and
    independent evidence about VP1: those markings converge where VP1 says they do, or
    one of the two is wrong.

    Near-vertical segments are dropped outright. They are the sides of kerbs, poles and
    sign posts; they belong to the vertical vanishing direction rather than to either
    road direction, and they are numerous enough to dominate a fit if left in.
    """
    vp1 = np.asarray(vp1, float)
    transverse: List[List[float]] = []
    along: List[List[float]] = []
    n_vert = 0
    for x1, y1, x2, y2 in segs:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) % 180
        if abs(angle - 90) < vertical_reject_deg:
            n_vert += 1
            continue
        mid = np.array([(x1 + x2) / 2.0, (y1 + y2) / 2.0])
        direction = np.array([x2 - x1, y2 - y1])
        to_vp = vp1 - mid
        cross = abs(direction[0] * to_vp[1] - direction[1] * to_vp[0]) / (
            np.linalg.norm(direction) * np.linalg.norm(to_vp) + 1e-9
        )
        if math.degrees(math.asin(min(1.0, cross))) < vp1_reject_deg:
            along.append([x1, y1, x2, y2])
        else:
            transverse.append([x1, y1, x2, y2])
    return (
        np.asarray(transverse, float).reshape(-1, 4),
        np.asarray(along, float).reshape(-1, 4),
        n_vert,
    )
