"""Self-calibrating a traffic camera from the road markings already painted on the road.

WHAT THIS IS FOR
    :mod:`speed_geometry_utils` needs two perpendicular vanishing points. Vehicle motion
    gives the first. Nothing about vehicle motion can give the second -- and an
    axis-aligned detection box carries no direction at all, since its bottom-centre and
    top-centre share an ``x``. The second one has to come from the image, which is what
    this module extracts.

    Transverse markings -- stop lines, zebra crossings, give-way triangles, turn arrows --
    run ACROSS the carriageway by construction, so their vanishing point IS VP2. They are
    also static, which is the real advantage: no motion, no tracking, no detector, and no
    dependence on vehicle edges, which is exactly what a camera looking along a road
    cannot resolve.

THREE THINGS THAT HAVE TO BE RIGHT, AND ARE EASY TO GET WRONG
    1. A marking is not simply BRIGHT. Dry asphalt is unsaturated and sits well above 130
       in value, so an absolute brightness threshold selects the entire carriageway. What
       distinguishes paint is that it is brighter than the road IMMEDIATELY AROUND IT and
       thin -- a morphological top-hat, not a threshold.
    2. A road scene is dominated by lines running ALONG the road: lane edges, kerbs,
       barriers, the road edge itself. They converge on VP1, not VP2, and they outnumber
       the transverse markings. :func:`split_by_vp1` removes them explicitly.
    3. VP2 sits near horizontal infinity, where WHICH SIDE of the principal point it lands
       on is the least reliable thing about it. Left unconstrained the fit lands on the
       wrong side and yields no real focal length at all. The search is restricted to
       candidates that actually calibrate against VP1 -- Dubska et al.'s conditional-VP
       fix, and the difference between unusable and usable.

WHY A BACKGROUND MODEL AND NOT A MEDIAN OF STORED FRAMES
    Paint has to be looked for on a road with no traffic on it. Offline one takes the
    median of sampled frames; in a live stream that would mean holding dozens of frames
    at full resolution -- over a hundred megabytes per camera. A running background model
    gives the same clean plate in bounded memory, which is the only version of this that
    can run per camera in a worker.
"""

import logging
import math
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

from .speed_geometry_utils import (
    DEFAULT_MAX_F_SENSITIVITY_PCT,  # noqa: F401  (re-exported)
    assess,
    focal_from_vps,
)
from .speed_paint_utils import (
    paint_mask,
    road_mask_from_points,
    segments_from_paint,
    split_by_vp1,
)

logger = logging.getLogger(__name__)


def _angle_between(a: np.ndarray, b: np.ndarray, pp: np.ndarray) -> float:
    """Angle between two vanishing points as seen from the principal point, in degrees."""
    u, v = np.asarray(a, float) - pp, np.asarray(b, float) - pp
    cos = float(u @ v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-12)
    return math.degrees(math.acos(max(-1.0, min(1.0, cos))))


def _lines_and_angles(segs: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(segs)
    p1 = np.hstack([segs[:, 0:2], np.ones((n, 1))])
    p2 = np.hstack([segs[:, 2:4], np.ones((n, 1))])
    lines = np.cross(p1, p2)
    lines = lines / np.maximum(np.linalg.norm(lines[:, :2], axis=1, keepdims=True), 1e-12)
    mids = (segs[:, 0:2] + segs[:, 2:4]) / 2.0
    angles = np.arctan2(segs[:, 3] - segs[:, 1], segs[:, 2] - segs[:, 0])
    return lines, mids, angles


def _dehomogenise(v: np.ndarray) -> Optional[np.ndarray]:
    return None if abs(v[2]) < 1e-12 else np.array([v[0] / v[2], v[1] / v[2]])


def vp_ransac(
    segs: np.ndarray,
    angle_tol_deg: float = 2.0,
    iters: int = 20000,
    seed: int = 0,
) -> Tuple[Optional[np.ndarray], np.ndarray]:
    """Vanishing point of a family of segments. Returns ``(vp, inlier mask)``.

    Scored by the ANGLE between each segment and the direction from its midpoint to the
    candidate, never by point-line distance. For a vanishing point near infinity -- the
    normal case for a road receding from the camera -- distance is enormous for every
    candidate and carries no information, while the angle stays meaningful throughout.
    """
    n = len(segs)
    if n < 2:
        return None, np.zeros(0, bool)
    lines, mids, angles = _lines_and_angles(segs)
    tol = math.radians(angle_tol_deg)
    rng = np.random.default_rng(seed)

    best_vp: Optional[np.ndarray] = None
    best_inl = np.zeros(n, bool)
    for _ in range(iters):
        i, j = rng.choice(n, 2, replace=False)
        point = _dehomogenise(np.cross(lines[i], lines[j]))
        if point is None:
            continue
        a = np.arctan2(point[1] - mids[:, 1], point[0] - mids[:, 0])
        d = np.abs(((a - angles) + np.pi / 2) % np.pi - np.pi / 2)
        inl = d < tol
        if inl.sum() > best_inl.sum():
            best_vp, best_inl = point, inl
    return best_vp, best_inl


def solve_vp2(
    segs: np.ndarray,
    vp1: np.ndarray,
    pp: np.ndarray,
    iters: int = 20000,
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """VP2 from the transverse segments, constrained to calibrate against VP1.

    Every candidate that does not yield a real focal length against VP1 is rejected
    outright -- that single test is what stops the fit landing on the wrong side of the
    principal point, which is where an unconstrained fit reliably goes.
    """
    if len(segs) < 2:
        return None
    lines, mids, angles = _lines_and_angles(segs)
    tol = math.radians(2.0)
    rng = np.random.default_rng(0)
    n = len(segs)

    best: Optional[Tuple[np.ndarray, np.ndarray]] = None
    for _ in range(iters):
        i, j = rng.choice(n, 2, replace=False)
        point = _dehomogenise(np.cross(lines[i], lines[j]))
        if point is None:
            continue
        if focal_from_vps((vp1[0], vp1[1]), (point[0], point[1]), (pp[0], pp[1])) is None:
            continue  # wrong side of the principal point: not a perpendicular pair
        a = np.arctan2(point[1] - mids[:, 1], point[0] - mids[:, 0])
        d = np.abs(((a - angles) + np.pi / 2) % np.pi - np.pi / 2)
        inl = d < tol
        if best is None or inl.sum() > best[1].sum():
            best = (point, inl)
    return best


def vp2_on_horizon(
    segs: np.ndarray,
    horizon_y: float,
    pp: np.ndarray,
    vp1: np.ndarray,
) -> Optional[Tuple[np.ndarray, int]]:
    """VP2 constrained to the road's vanishing line. One free parameter, not two.

    VP1 and VP2 are both directions ON the road, so both lie on the road's vanishing
    line -- and with no camera roll, which every method in this family assumes, that line
    is the image row through VP1. Fitting VP2 freely in 2D ignores that and spends its
    second degree of freedom on noise: measured on a synthetic camera with known truth,
    the free fit put VP2 118 px off the horizon that VP1 defines and the focal length came
    out 22 % high.

    Here each transverse segment is intersected with the horizon row, giving one candidate
    ``x`` apiece, and the median is taken. A median because a single mis-classified
    along-road segment is nearly parallel to the horizon and intersects it absurdly far
    away -- exactly the outlier a mean would chase.
    """
    if len(segs) < 2:
        return None
    xs = []
    for x1, y1, x2, y2 in segs:
        dy = y2 - y1
        if abs(dy) < 1e-6:
            continue  # parallel to the horizon: no usable intersection
        xs.append(x1 + (x2 - x1) * (horizon_y - y1) / dy)
    if len(xs) < 2:
        return None
    vp2 = np.array([float(np.median(xs)), float(horizon_y)])
    if focal_from_vps((vp1[0], vp1[1]), (vp2[0], vp2[1]), (pp[0], pp[1])) is None:
        return None
    spread = float(np.median(np.abs(np.asarray(xs) - vp2[0])))
    inliers = int(np.sum(np.abs(np.asarray(xs) - vp2[0]) <= max(spread * 3.0, 50.0)))
    return vp2, inliers


def track_chords(
    tracks: Dict[int, List[Tuple[float, float]]],
    min_points: int = 6,
    min_length_px: float = 40.0,
) -> np.ndarray:
    """One chord per track: first observed ground point to last, in pixels.

    A chord rather than every consecutive pair. Consecutive points are a few pixels apart
    and their direction is mostly jitter; the chord of a whole track is a long baseline
    whose direction is the direction the vehicle actually travelled. Short tracks and
    short chords are dropped for the same reason -- they are id noise, and they vote.
    """
    chords = []
    for points in tracks.values():
        if len(points) < min_points:
            continue
        (x1, y1), (x2, y2) = points[0], points[-1]
        if math.hypot(x2 - x1, y2 - y1) >= min_length_px:
            chords.append([x1, y1, x2, y2])
    return np.asarray(chords, float).reshape(-1, 4)


class CalibrationResult:
    """The outcome of one calibration attempt: either a camera, or why there isn't one."""

    def __init__(
        self,
        vp1: Optional[Tuple[float, float]] = None,
        vp2: Optional[Tuple[float, float]] = None,
        focal: Optional[float] = None,
        reason: str = "",
        permanent: bool = False,
        diagnostics: Optional[Dict[str, float]] = None,
    ) -> None:
        self.vp1 = vp1
        self.vp2 = vp2
        self.focal = focal
        self.reason = reason
        #: True when retrying cannot help -- the scene has no transverse markings, or the
        #: camera angle makes the across-road direction unmeasurable. Retrying such a
        #: camera every few hundred frames burns CPU forever for an answer that will not
        #: change, so the caller stops.
        self.permanent = permanent
        self.diagnostics = diagnostics or {}

    @property
    def ok(self) -> bool:
        return self.vp1 is not None and self.vp2 is not None and self.focal is not None


class SelfCalibrator:
    """Accumulates a background plate and vehicle tracks, then recovers the camera.

    Deliberately stateful and per camera. It holds one background model and a bounded
    number of track chords, and nothing else -- no frames are retained, which is what
    makes it affordable to run one of these per stream.
    """

    def __init__(
        self,
        min_frames: int = 150,
        min_tracks: int = 25,
        max_tracks: int = 400,
        retry_interval_frames: int = 300,
        max_attempts: int = 5,
        tophat: int = 35,
        tophat_thresh: int = 22,
        roi_top: float = 0.30,
        min_len: int = 30,
        vp1_reject_deg: float = 12.0,
        max_vp2_diagonals: float = 20.0,
        max_f_sensitivity_pct: float = DEFAULT_MAX_F_SENSITIVITY_PCT,
    ) -> None:
        self.min_frames = min_frames
        self.min_tracks = min_tracks
        self.max_tracks = max_tracks
        self.retry_interval_frames = retry_interval_frames
        self.max_attempts = max_attempts
        self.tophat = tophat
        self.tophat_thresh = tophat_thresh
        self.roi_top = roi_top
        self.min_len = min_len
        self.vp1_reject_deg = vp1_reject_deg
        self.max_vp2_diagonals = max_vp2_diagonals
        self.max_f_sensitivity_pct = max_f_sensitivity_pct

        self._bg = cv2.createBackgroundSubtractorMOG2(history=min_frames, detectShadows=False)
        self._frames = 0
        self._attempts = 0
        self._next_attempt_at = min_frames
        self._tracks: Dict[int, List[Tuple[float, float]]] = {}
        self._ground_points: List[Tuple[float, float]] = []
        self.result: Optional[CalibrationResult] = None

    @property
    def done(self) -> bool:
        """True once there is a camera, or once it is established there will not be one."""
        return self.result is not None and (self.result.ok or self.result.permanent)

    def observe_frame(self, frame: np.ndarray) -> None:
        """Feed one frame into the background model. Cheap; safe to call per frame."""
        self._bg.apply(frame)
        self._frames += 1

    def observe_track(self, track_id: int, x: float, y: float) -> None:
        """Record one vehicle ground point, in pixels, for the VP1 fit."""
        if track_id in self._tracks:
            self._tracks[track_id].append((x, y))
        elif len(self._tracks) < self.max_tracks:
            self._tracks[track_id] = [(x, y)]
        else:
            return
        if len(self._ground_points) < self.max_tracks * 20:
            self._ground_points.append((x, y))

    def ready(self) -> bool:
        """Is there enough evidence to be worth attempting a calibration?"""
        if self.done or self._attempts >= self.max_attempts:
            return False
        return self._frames >= self._next_attempt_at and len(self._tracks) >= self.min_tracks

    def _paint_families(self, background, vp1, width: int, height: int):
        """Extract the paint, split it by direction, and refine VP1 from the along-road half.

        Returns ``(segments, transverse, along_road, vp1, vp1_refit_degrees)``.

        The refit uses the vehicle-chord VP1 only to CLASSIFY the segments, then re-fits
        VP1 from the along-road paint itself. Painted lane lines are static,
        high-contrast and span the frame; a vehicle chord is a short, noisy baseline
        between two boxes whose edges wobble. Where there is enough paint it is the
        better instrument, and VP1's error propagates into the focal length.
        """
        pp = np.array([width / 2.0, height / 2.0])
        road = road_mask_from_points(self._ground_points, width, height)
        mask = paint_mask(background, self.tophat, self.tophat_thresh, self.roi_top, road)
        segs = segments_from_paint(mask, self.min_len)
        trans, along, _ = split_by_vp1(segs, vp1, self.vp1_reject_deg)

        vp1_refit_deg = 0.0
        if len(along) >= 6:
            refit, refit_inl = vp_ransac(along, angle_tol_deg=2.0, iters=20000, seed=0)
            if refit is not None and int(refit_inl.sum()) >= 4:
                vp1_refit_deg = _angle_between(vp1, refit, pp)
                vp1 = refit
                # The classification used the rougher VP1, so redo it now that the better
                # one is available: a segment on the boundary may change family.
                trans, along, _ = split_by_vp1(segs, vp1, self.vp1_reject_deg)
        return segs, trans, along, vp1, vp1_refit_deg

    def attempt(self, width: int, height: int) -> CalibrationResult:
        """Try once to recover the camera. Expensive; call only when :meth:`ready`."""
        self._attempts += 1
        self._next_attempt_at = self._frames + self.retry_interval_frames
        last = self._attempts >= self.max_attempts

        background = self._bg.getBackgroundImage()
        if background is None:
            self.result = CalibrationResult(reason="background model is not ready yet")
            return self.result

        pp = np.array([width / 2.0, height / 2.0])
        chords = track_chords(self._tracks)
        if len(chords) < 10:
            self.result = CalibrationResult(
                reason=f"only {len(chords)} usable vehicle tracks so far; VP1 needs more",
                permanent=last,
            )
            return self.result

        vp1, vp1_inl = vp_ransac(chords, angle_tol_deg=2.0, iters=20000, seed=0)
        if vp1 is None:
            self.result = CalibrationResult(
                reason="vehicle tracks do not converge on a single direction: the road "
                "may be curved, or this view covers a junction",
                permanent=last,
            )
            return self.result

        segs, trans, along, vp1, vp1_refit_deg = self._paint_families(
            background, vp1, width, height
        )

        diagnostics = {
            "frames": float(self._frames),
            "tracks": float(len(self._tracks)),
            "vp1_inliers": float(int(vp1_inl.sum())),
            "paint_segments": float(len(segs)),
            "along_road_segments": float(len(along)),
            "transverse_segments": float(len(trans)),
        }

        if len(trans) < 6:
            self.result = CalibrationResult(
                reason=(
                    f"no transverse road markings in view ({len(trans)} found, 6 needed; "
                    f"{len(along)} along-road markings were seen and correctly ignored). "
                    "This camera has no stop line, crossing, give-way triangle or arrow "
                    "in view -- typical of a motorway mainline. Speed cannot be measured "
                    "by this method here."
                ),
                permanent=last,
                diagnostics=diagnostics,
            )
            return self.result

        # Constrained to the horizon VP1 defines -- see vp2_on_horizon for why the free
        # 2D fit is not good enough.
        best = vp2_on_horizon(trans, float(vp1[1]), pp, vp1)
        if best is None:
            self.result = CalibrationResult(
                reason="no across-road vanishing point consistent with the traffic "
                "direction could be found in the transverse markings",
                permanent=last,
                diagnostics=diagnostics,
            )
            return self.result

        vp2, vp2_inliers = best
        diagnostics["vp2_inliers"] = float(vp2_inliers)
        diagnostics["vp1_refit_deg"] = vp1_refit_deg
        quality = assess(
            (vp1[0], vp1[1]),
            (vp2[0], vp2[1]),
            (pp[0], pp[1]),
            float(width),
            float(height),
            self.max_vp2_diagonals,
            self.max_f_sensitivity_pct,
        )
        diagnostics["vp2_distance_px"] = quality.vp2_distance_px
        diagnostics["f_sensitivity_pct"] = quality.f_sensitivity_pct

        if not quality.ok:
            self.result = CalibrationResult(
                reason=quality.reason,
                # A degenerate camera angle does not improve with more frames. This is a
                # property of where the camera points, not of how long it has watched.
                permanent=True,
                diagnostics=diagnostics,
            )
            return self.result

        self.result = CalibrationResult(
            vp1=(float(vp1[0]), float(vp1[1])),
            vp2=(float(vp2[0]), float(vp2[1])),
            focal=quality.focal,
            diagnostics=diagnostics,
        )
        # The evidence has done its job; a calibrated camera never needs it again, and
        # holding it would keep a few hundred track histories alive for the life of the
        # stream.
        self._tracks.clear()
        self._ground_points.clear()
        return self.result
