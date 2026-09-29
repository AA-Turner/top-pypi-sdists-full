"""Calibrating a traffic camera from the 3D boxes of the vehicles themselves.

THE FALLBACK, AND WHY IT EXISTS
    :mod:`speed_paint_calibration_utils` recovers the camera from painted TRANSVERSE
    markings, and says honestly when a scene has none -- a motorway mainline is the
    textbook case. A detector that regresses each vehicle's 3D box (UrbanOmniDetect, via
    ml-codebases' ``urbanomnidetect_code_base``) hands this use case something those
    markings were only ever a proxy for: every car's ground footprint, four points where
    the wheels meet the road, on a rectangle of roughly known size.

THE METHOD (Revaud & Humenberger's energy minimisation, reduced to four unknowns)
    A pinhole camera, principal point at the image centre, square pixels, over a flat
    road. Its pose relative to the road is a tilt ``theta`` and a roll ``phi`` -- yaw is
    unobservable and absorbed into the world frame -- plus a height ``h``. With the focal
    length ``f`` that is four unknowns. Each footprint, mapped onto the road through a
    candidate camera, should be a rectangle of ``car_length_m`` x ``car_width_m`` with a
    right angle at its corners. Hundreds of footprints from many cars at many depths are
    fitted at once with a robust loss, so odd vehicles and bad corners do not dominate.

    Metric scale comes out of the car size, in metres, so ``h`` is SOLVED rather than
    surveyed -- the installer's ``camera_height_m`` only seeds the search.

    Which of a footprint's two side pairs is its length is decided per footprint in
    metric space (the longer one), so the fit does not depend on the detector's corner
    labelling -- only on the four corners being in cyclic order around the footprint.

WHERE ALONG-ROAD COMES FROM
    Speed is the rate of change of the ALONG-road coordinate. With no vanishing point the
    road direction is not known a priori, but every car is parked along it: the median
    direction of the footprints' long sides, averaged as a doubled angle so that a side
    and its reverse agree, is the road direction.

WHAT IT CANNOT DO
    It assumes cars of roughly one size. A 10 % error in the assumed length is a 10 %
    error in every speed, uniformly -- the same kind of error ``camera_height_m`` carries
    in the paint method. That is why only ``car`` footprints calibrate (trucks and buses
    are still MEASURED once the camera is known), and why the fit is refused when the
    footprints it produces do not come out car-sized.
"""

import logging
from math import atan2, cos, hypot, radians, sin
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

logger = logging.getLogger(__name__)

#: Starting tilts for the solver, in degrees below the horizontal. The fit is local, so a
#: handful of starts covers everything from a pole-top camera to a gantry looking down.
_TILT_STARTS_DEG = (10.0, 25.0, 45.0, 70.0)

#: Focal-length starts, as multiples of the image width.
_FOCAL_STARTS = (0.7, 1.2, 2.0)

#: Footprints fed to one solve. More adds time, not accuracy.
_SOLVE_SAMPLE = 600

#: A footprint's shorter image side must be at least this long for it to count when the
#: solved camera is JUDGED (it still helps the fit either way).
_JUDGE_MIN_SIDE_PX = 15.0


def _rotation(tilt: float, roll: float) -> np.ndarray:
    """World -> camera rotation. Rows are the camera's x, y, z axes in world coordinates.

    World: X right, Y forward along the ground, Z up; the road is ``Z = 0``. Camera: x
    right, y down, z forward -- the image convention. ``tilt`` pitches the optical axis
    below the horizon; ``roll`` turns the image about it.
    """
    xc = np.array([1.0, 0.0, 0.0])
    yc = np.array([0.0, -sin(tilt), -cos(tilt)])
    zc = np.array([0.0, cos(tilt), -sin(tilt)])
    xr = cos(roll) * xc + sin(roll) * yc
    yr = -sin(roll) * xc + cos(roll) * yc
    return np.stack([xr, yr, zc])


def _to_ground(
    uv: np.ndarray, f: float, pp: Tuple[float, float], rot: np.ndarray, h: float
) -> Tuple[np.ndarray, np.ndarray]:
    """Pixels ``(..., 2)`` -> road points ``(..., 2)`` in metres, and a valid mask.

    A pixel is valid when its viewing ray points below the horizon, i.e. meets the road in
    front of the camera. Invalid points come back as zeros; callers check the mask.
    """
    d_cam = np.stack(
        [(uv[..., 0] - pp[0]) / f, (uv[..., 1] - pp[1]) / f, np.ones(uv.shape[:-1])], axis=-1
    )
    d_w = d_cam @ rot  # R^T d, row-vector form
    dz = d_w[..., 2]
    valid = dz < -1e-9
    lam = np.where(valid, -h / np.where(valid, dz, -1.0), 0.0)
    return lam[..., None] * d_w[..., :2], valid


def _footprint_residuals(
    params: np.ndarray,
    uv: np.ndarray,
    pp: Tuple[float, float],
    length_m: float,
    width_m: float,
) -> np.ndarray:
    """Per footprint: relative length error, relative width error, corner cosine."""
    f, tilt, roll, h = params
    ground, valid = _to_ground(uv, f, pp, _rotation(tilt, roll), h)
    edges = np.roll(ground, -1, axis=1) - ground  # 0->1, 1->2, 2->3, 3->0
    n = np.linalg.norm(edges, axis=2) + 1e-9
    pair_a = 0.5 * (n[:, 0] + n[:, 2])
    pair_b = 0.5 * (n[:, 1] + n[:, 3])
    # Signed, not |cos|: corner jitter makes |cos| positive on average, and the fit would
    # tilt the camera to "straighten" noise. Signed, the noise averages out.
    cosang = (edges[:, 0] * edges[:, 1]).sum(axis=1) / (n[:, 0] * n[:, 1])
    res = np.stack(
        [
            (np.maximum(pair_a, pair_b) - length_m) / length_m,
            (np.minimum(pair_a, pair_b) - width_m) / width_m,
            cosang,
        ],
        axis=1,
    )
    res[~valid.all(axis=1)] = 1.0  # a corner above the horizon: this camera is wrong
    return res.ravel()


class Box3DPlane:
    """Maps a pixel to ``(along, across)`` metres on the road, like ``RoadPlane``.

    Same interface as :class:`speed_geometry_utils.RoadPlane` -- ``project`` and
    ``metres_per_pixel`` -- so the fitting and uncertainty code runs on either unchanged.
    """

    def __init__(
        self,
        pp: Tuple[float, float],
        focal: float,
        tilt: float,
        roll: float,
        height_m: float,
        road_angle: float = 0.0,
    ) -> None:
        self.pp = pp
        self.f = focal
        self.tilt = tilt
        self.roll = roll
        self.height_m = height_m
        self.road_angle = road_angle
        self._rot = _rotation(tilt, roll)

    def ground(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        """Pixel -> world ``(X, Y)`` metres on the road, or ``None`` above the horizon."""
        pts, valid = _to_ground(
            np.array([[x, y]], float), self.f, self.pp, self._rot, self.height_m
        )
        if not bool(valid[0]):
            return None
        return float(pts[0, 0]), float(pts[0, 1])

    def project(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        """Pixel -> ``(along, across)`` in METRES, along being the road direction."""
        g = self.ground(x, y)
        if g is None:
            return None
        c, s = cos(self.road_angle), sin(self.road_angle)
        return g[0] * c + g[1] * s, -g[0] * s + g[1] * c

    def metres_per_pixel(self, x: float, y: float, pixels: float) -> float:
        """Ground metres spanned by ``pixels`` of vertical wobble at this image point."""
        here = self.project(x, y)
        there = self.project(x, y + pixels)
        if here is None or there is None:
            return 0.0
        return hypot(there[0] - here[0], there[1] - here[1])

    def pixel(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """World ``(X, Y)`` on the road -> pixel. The inverse of :meth:`ground`."""
        p = self._rot @ (np.array([world_x, world_y, 0.0]) - np.array([0.0, 0.0, self.height_m]))
        return self.pp[0] + self.f * p[0] / p[2], self.pp[1] + self.f * p[1] / p[2]


class Box3DResult:
    """One solve: a plane, or the reason there is none."""

    def __init__(
        self,
        plane: Optional[Box3DPlane] = None,
        reason: str = "",
        diagnostics: Optional[Dict[str, float]] = None,
    ) -> None:
        self.plane = plane
        self.reason = reason
        self.diagnostics = diagnostics or {}

    @property
    def ok(self) -> bool:
        return self.plane is not None


def solve_camera(
    footprints: np.ndarray,
    width: int,
    height: int,
    car_length_m: float = 4.5,
    car_width_m: float = 1.8,
    init_height_m: float = 8.0,
    max_dim_error: float = 0.15,
) -> Box3DResult:
    """Fit ``(f, tilt, roll, h)`` to ``footprints`` -- ``(N, 4, 2)`` pixels, cyclic order."""
    from scipy.optimize import least_squares  # noqa: PLC0415  (only while calibrating)

    pp = (width / 2.0, height / 2.0)
    if len(footprints) > _SOLVE_SAMPLE:
        idx = np.random.default_rng(0).choice(len(footprints), _SOLVE_SAMPLE, replace=False)
        footprints = footprints[idx]
    lower = [0.2 * width, radians(1.0), radians(-30.0), 0.5]
    upper = [6.0 * width, radians(89.0), radians(30.0), 100.0]

    best = None
    for tilt_deg in _TILT_STARTS_DEG:
        for f_mult in _FOCAL_STARTS:
            x0 = [f_mult * width, radians(tilt_deg), 0.0, float(init_height_m)]
            x0 = [
                min(max(v, lo * 1.0001), hi * 0.9999)
                for v, lo, hi in zip(x0, lower, upper, strict=True)
            ]
            fit = least_squares(
                _footprint_residuals,
                x0,
                bounds=(lower, upper),
                loss="soft_l1",
                f_scale=0.1,
                args=(footprints, pp, car_length_m, car_width_m),
                max_nfev=400,
            )
            if best is None or fit.cost < best.cost:
                best = fit
    assert best is not None  # noqa: S101 - the loops above always run
    camera = _refine_in_image(best.x, footprints, pp, car_length_m, car_width_m, lower, upper)
    f, tilt, roll, h = (float(v) for v in camera)
    # Judged on the footprints measured well enough to judge by: the shorter image side at
    # least _JUDGE_MIN_SIDE_PX. On a far car a pixel of jitter is a large share of that
    # side and it inflates the implied size, so including them rejects good cameras.
    edges = np.linalg.norm(np.roll(footprints, -1, axis=1) - footprints, axis=2)
    short = np.minimum(edges[:, 0] + edges[:, 2], edges[:, 1] + edges[:, 3]) / 2.0
    judged = footprints[short >= _JUDGE_MIN_SIDE_PX]
    if len(judged) < 10:
        judged = footprints
    res = _footprint_residuals(camera, judged, pp, car_length_m, car_width_m).reshape(-1, 3)
    diagnostics = {
        "footprints": float(len(footprints)),
        "judged_footprints": float(len(judged)),
        "focal_px": f,
        "tilt_deg": float(np.degrees(tilt)),
        "roll_deg": float(np.degrees(roll)),
        "camera_height_m": h,
        "median_length_err_pct": 100.0 * float(np.median(np.abs(res[:, 0]))),
        "median_width_err_pct": 100.0 * float(np.median(np.abs(res[:, 1]))),
        "median_corner_cos": float(np.median(np.abs(res[:, 2]))),
    }
    if (
        diagnostics["median_length_err_pct"] > 100.0 * max_dim_error
        or diagnostics["median_width_err_pct"] > 150.0 * max_dim_error
        # Loose on purpose: corner jitter alone pushes this to ~0.25 at 3 px, while the size
        # checks above are what a wrong camera actually fails.
        or diagnostics["median_corner_cos"] > 0.4
    ):
        return Box3DResult(
            reason=(
                "the vehicle footprints do not fit one camera: median length error "
                f"{diagnostics['median_length_err_pct']:.0f} %, width error "
                f"{diagnostics['median_width_err_pct']:.0f} %, corner cosine "
                f"{diagnostics['median_corner_cos']:.2f}. Too few cars, cars too far away, "
                "or the 3D corners are too noisy on this view."
            ),
            diagnostics=diagnostics,
        )
    plane = Box3DPlane(pp, f, tilt, roll, h)
    plane.road_angle = _road_angle(plane, footprints)
    diagnostics["road_angle_deg"] = float(np.degrees(plane.road_angle))
    return Box3DResult(plane=plane, diagnostics=diagnostics)


def _rectangles(poses: np.ndarray, sides: np.ndarray, hand: np.ndarray) -> np.ndarray:
    """Road-plane corners ``(N, 4, 2)`` of rectangles in the detector's cyclic order.

    ``poses`` is ``(N, 3)``: centre X, centre Y, and the heading of the 0->1 side.
    ``sides`` is ``(N, 2)``: the 0->1 and 1->2 side lengths. ``hand`` is +-1, whether
    1->2 turns left or right of 0->1 -- fixed from the initial solve, like ``sides``, so
    the rectangle keeps the detector's corner labelling and needs no matching.
    """
    c, s = np.cos(poses[:, 2]), np.sin(poses[:, 2])
    u = np.stack([c, s], axis=1)
    v = hand[:, None] * np.stack([-s, c], axis=1)
    a, b = sides[:, :1], sides[:, 1:]
    c0 = poses[:, :2] - 0.5 * a * u - 0.5 * b * v
    c1 = c0 + a * u
    return np.stack([c0, c1, c1 + b * v, c0 + b * v], axis=1)


def _to_pixels(ground: np.ndarray, camera: np.ndarray, pp: Tuple[float, float]) -> np.ndarray:
    """Road points ``(..., 2)`` -> pixels ``(..., 2)`` through ``camera = (f, tilt, roll, h)``."""
    f, tilt, roll, h = camera
    rot = _rotation(tilt, roll)
    pc = ground[..., :1] * rot[:, 0] + ground[..., 1:2] * rot[:, 1] - h * rot[:, 2]
    z = np.maximum(pc[..., 2], 1e-6)  # behind the camera: pinned, and far from any corner
    return np.stack([pp[0] + f * pc[..., 0] / z, pp[1] + f * pc[..., 1] / z], axis=-1)


def _refine_in_image(
    camera0: np.ndarray,
    footprints: np.ndarray,
    pp: Tuple[float, float],
    length_m: float,
    width_m: float,
    lower: List[float],
    upper: List[float],
) -> np.ndarray:
    """Re-fit the camera by REPROJECTION error, in pixels, starting from ``camera0``.

    The road-space fit above measures noisy edges after mapping them onto the road, and a
    noisy edge always comes out long -- the norm of a noisy vector is biased up. So that
    fit shrinks the scale, and every speed reads a few percent low (-3 to -4 % at 1 px of
    corner jitter, measured on the synthetic camera). Here each car is a rectangle of the
    assumed size with its own position and heading, projected INTO the image and
    compared with the detected corners, so pixel noise stays zero-mean where it is
    measured. That is the maximum-likelihood fit under pixel noise, and it removes the
    bias; the road-space fit is only its starting point.
    """
    from scipy.optimize import least_squares  # noqa: PLC0415
    from scipy.sparse import lil_matrix  # noqa: PLC0415

    n = len(footprints)
    ground, valid = _to_ground(
        footprints, camera0[0], pp, _rotation(camera0[1], camera0[2]), camera0[3]
    )
    keep = valid.all(axis=1)
    if int(keep.sum()) < 10:
        return camera0
    footprints, ground, n = footprints[keep], ground[keep], int(keep.sum())
    e01 = ground[:, 1] - ground[:, 0]
    e12 = ground[:, 2] - ground[:, 1]
    hand = np.sign(e01[:, 0] * e12[:, 1] - e01[:, 1] * e12[:, 0])
    hand[hand == 0] = 1.0
    edges = np.linalg.norm(np.roll(ground, -1, axis=1) - ground, axis=2)
    first_is_long = (edges[:, 0] + edges[:, 2]) >= (edges[:, 1] + edges[:, 3])
    sides = np.where(first_is_long[:, None], [[length_m, width_m]], [[width_m, length_m]]).astype(
        float
    )
    poses = np.concatenate([ground.mean(axis=1), np.arctan2(e01[:, 1], e01[:, 0])[:, None]], axis=1)

    def residuals(x: np.ndarray) -> np.ndarray:
        rect = _rectangles(x[4:].reshape(n, 3), sides, hand)
        return (_to_pixels(rect, x[:4], pp) - footprints).ravel()

    sparsity = lil_matrix((8 * n, 4 + 3 * n), dtype=int)
    sparsity[:, :4] = 1
    for i in range(n):
        sparsity[8 * i : 8 * i + 8, 4 + 3 * i : 7 + 3 * i] = 1
    inf = np.full(3 * n, np.inf)
    x0 = np.concatenate([np.clip(camera0, lower, upper), poses.ravel()])
    fit = least_squares(
        residuals,
        x0,
        jac_sparsity=sparsity,
        bounds=(np.concatenate([lower, -inf]), np.concatenate([upper, inf])),
        loss="soft_l1",
        f_scale=2.0,  # pixels: a corner more than ~2 px off is treated as an outlier
        x_scale="jac",
        max_nfev=200,
    )
    return fit.x[:4] if fit.success or fit.status == 0 else camera0


def _road_angle(plane: Box3DPlane, footprints: np.ndarray) -> float:
    """Median direction of the footprints' long sides on the road, in radians."""
    ground, valid = _to_ground(footprints, plane.f, plane.pp, plane._rot, plane.height_m)
    ok = valid.all(axis=1)
    ground = ground[ok]
    if len(ground) == 0:
        return 0.0
    edges = np.roll(ground, -1, axis=1) - ground
    n = np.linalg.norm(edges, axis=2)
    use_a = (n[:, 0] + n[:, 2]) >= (n[:, 1] + n[:, 3])
    long_edge = np.where(use_a[:, None], edges[:, 0], edges[:, 1])
    doubled = 2.0 * np.arctan2(long_edge[:, 1], long_edge[:, 0])
    return 0.5 * atan2(float(np.median(np.sin(doubled))), float(np.median(np.cos(doubled))))


def footprint(
    det: Dict[str, Any],
    ground_indices: Sequence[int],
    width: int,
    height: int,
    min_corner_conf: float = 0.5,
    min_size_px: float = 12.0,
    margin_px: float = 2.0,
) -> Optional[np.ndarray]:
    """The 4 ground-contact corners of a detection, ``(4, 2)`` pixels, or ``None``.

    ``None`` for anything that is not a trustworthy footprint: no keypoints, a corner
    below ``min_corner_conf``, a corner outside the frame (a vehicle cut off at the edge
    has corners the detector guessed), or a footprint too small to measure. Keypoints
    that arrive normalised (every coordinate within the unit square) are scaled up.
    """
    kpts = det.get("keypoints")
    if not isinstance(kpts, (list, tuple)) or len(kpts) <= max(ground_indices):
        return None
    corners = []
    for i in ground_indices:
        p = kpts[i]
        if not isinstance(p, (list, tuple)) or len(p) < 2:
            return None
        if len(p) >= 3 and float(p[2]) < min_corner_conf:
            return None
        corners.append((float(p[0]), float(p[1])))
    pts = np.asarray(corners, float)
    if float(np.abs(pts).max()) <= 1.5 and max(width, height) > 2:
        pts = pts * np.array([width, height], float)
    if (
        pts[:, 0].min() < margin_px
        or pts[:, 1].min() < margin_px
        or pts[:, 0].max() > width - margin_px
        or pts[:, 1].max() > height - margin_px
    ):
        return None
    span = pts.max(axis=0) - pts.min(axis=0)
    if hypot(float(span[0]), float(span[1])) < min_size_px:
        return None
    return pts


class Box3DFallback:
    """Collects car footprints from the first frame; solves the camera once triggered.

    Triggered when the paint calibration has not produced a camera within
    ``after_seconds`` of frame time, or has declared the camera uncalibratable. Collection
    starts at once, so a camera that needs the fallback has its evidence ready by then.
    """

    def __init__(
        self,
        enabled: bool = True,
        after_seconds: float = 60.0,
        ground_indices: Sequence[int] = (0, 1, 2, 3),
        categories: Sequence[str] = ("car",),
        car_length_m: float = 4.5,
        car_width_m: float = 1.8,
        init_height_m: float = 8.0,
        min_footprints: int = 300,
        min_tracks: int = 20,
        retry_footprints: int = 300,
        max_footprints: int = 3000,
        min_corner_conf: float = 0.5,
        min_size_px: float = 12.0,
        max_dim_error: float = 0.15,
    ) -> None:
        self.enabled = enabled
        self.after_seconds = after_seconds
        self.ground_indices = tuple(ground_indices)
        self.categories = {c.lower() for c in categories}
        self.car_length_m = car_length_m
        self.car_width_m = car_width_m
        self.init_height_m = init_height_m
        self.min_footprints = min_footprints
        self.min_tracks = min_tracks
        self.retry_footprints = retry_footprints
        self.max_footprints = max_footprints
        self.min_corner_conf = min_corner_conf
        self.min_size_px = min_size_px
        self.max_dim_error = max_dim_error

        self.plane: Optional[Box3DPlane] = None
        self.result: Optional[Box3DResult] = None
        self.triggered = False
        self._first_ts: Optional[float] = None
        self._footprints: List[np.ndarray] = []
        self._seen = 0
        self._tracks: set = set()
        self._next_attempt_at = min_footprints

    @property
    def footprints_seen(self) -> int:
        """Usable footprints received so far. 0 means the detector sends no 3D corners."""
        return self._seen

    def corners(self, det: Dict[str, Any], width: int, height: int) -> Optional[np.ndarray]:
        """This detection's footprint under this fallback's settings."""
        return footprint(
            det,
            self.ground_indices,
            width,
            height,
            self.min_corner_conf,
            self.min_size_px,
        )

    def observe(
        self,
        detections: List[Dict[str, Any]],
        frame_ts: float,
        width: int,
        height: int,
        paint_failed: bool,
    ) -> bool:
        """Collect this frame's footprints; solve when due. True the frame it succeeds."""
        if not self.enabled or self.plane is not None:
            return False
        if self._first_ts is None:
            self._first_ts = frame_ts
        for det in detections:
            if str(det.get("category", "")).lower() not in self.categories:
                continue
            if det.get("track_id") is None:
                continue
            pts = self.corners(det, width, height)
            if pts is None:
                continue
            self._seen += 1
            self._tracks.add(det["track_id"])
            if len(self._footprints) < self.max_footprints:
                self._footprints.append(pts)
            else:  # ring: recent traffic replaces old, memory stays bounded
                self._footprints[self._seen % self.max_footprints] = pts

        self.triggered = (
            self.triggered or paint_failed or (frame_ts - self._first_ts >= self.after_seconds)
        )
        if not self.triggered or not self._ready():
            return False
        self._next_attempt_at = self._seen + self.retry_footprints
        self.result = solve_camera(
            np.stack(self._footprints),
            width,
            height,
            self.car_length_m,
            self.car_width_m,
            self.init_height_m,
            self.max_dim_error,
        )
        if self.result.ok:
            self.plane = self.result.plane
            self._footprints.clear()
            self._tracks.clear()
            return True
        logger.warning("vehicle_speed_estimation 3D-box fallback: %s", self.result.reason)
        return False

    def _ready(self) -> bool:
        return (
            len(self._footprints) >= self.min_footprints
            and len(self._tracks) >= self.min_tracks
            and self._seen >= self._next_attempt_at
        )

    def locate(
        self, det: Dict[str, Any], width: int, height: int
    ) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """``(pixel, (along, across))`` of this vehicle's footprint centre, or ``None``.

        The centre of the four ground corners, each mapped onto the road first: on the
        road, so free of the height bias a box edge carries, and not tied to whichever
        corner happens to be lowest in the image.
        """
        if self.plane is None:
            return None
        pts = self.corners(det, width, height)
        if pts is None:
            return None
        ground = [self.plane.project(float(x), float(y)) for x, y in pts]
        if any(g is None for g in ground):
            return None
        along = sum(g[0] for g in ground if g is not None) / 4.0
        across = sum(g[1] for g in ground if g is not None) / 4.0
        centre = pts.mean(axis=0)
        return (float(centre[0]), float(centre[1])), (along, across)
