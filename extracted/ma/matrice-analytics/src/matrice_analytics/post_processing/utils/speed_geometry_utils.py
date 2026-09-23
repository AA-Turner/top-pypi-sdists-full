"""Road-plane geometry for vehicle speed estimation, recovered from two vanishing points.

WHY THIS LIVES IN py_analytics AND NOT IN ml-applications
    An ml-applications app receives detection boxes and nothing else. The method below
    needs the actual frame: the across-road vanishing point is recovered from painted
    road markings, which are pixels. That is the whole reason this use case is here
    rather than there.

THE GEOMETRY, IN ORDER
    VP1     where the traffic direction vanishes. Vehicles on a straight road travel in
            parallel lines, so their trajectories converge there.
    VP2     where the ACROSS-road direction vanishes. Recovered from transverse painted
            markings -- stop lines, zebra crossings, give-way triangles, turn arrows --
            which run across the carriageway by construction.
    f       from orthogonality. Two perpendicular world directions project to two VPs
            whose offsets from the principal point satisfy (U-P).(V-P) = -f^2, so
            f = sqrt(-(U-P).(V-P)) -- Dubska et al., IEEE T-ITS 2015, eq. (4).
    normal  the vertical vanishing direction, which IS the road plane's normal.
    lam     the one real-world number. Metres per road unit, numerically equal to the
            camera's perpendicular height above the road surface. It can never be
            recovered from an image: a camera cannot tell a road from a scale model of
            a road.

WHY THE GATE IS NOT OPTIONAL
    f falls out of VP1 and VP2 together and is meaningless from either alone. A camera
    that looks nearly ALONG the road sees almost no variation in the across-road
    direction, so VP2 runs off towards infinity and the f it implies is noise. Dubska et
    al. say so outright: "when one of the first two VPs is in infinity, the focal length
    and the third VP cannot be calculated." :func:`assess` is that statement made
    executable. Without it a bad camera yields speeds that look entirely ordinary and are
    wrong by an unbounded factor, and nothing downstream could ever reveal it.

DEPENDENCIES
    Stdlib only, deliberately. This runs per frame; the OpenCV half of the method lives
    in :mod:`speed_paint_calibration_utils` and runs only while a camera is calibrating.
"""

from math import hypot, isfinite, sqrt
from typing import Optional, Tuple

#: An (x, y) pixel.
Point = Tuple[float, float]

#: A direction or a point in camera coordinates.
Vec3 = Tuple[float, float, float]

#: Past this many image diagonals, VP2 is an ideal point in all but name.
DEFAULT_MAX_VP2_DIAGONALS = 20.0

#: Past this, one pixel of VP1 error moves the focal length -- and every speed with it --
#: by more than a tolerable amount.
DEFAULT_MAX_F_SENSITIVITY_PCT = 2.0


def focal_from_vps(vp1: Point, vp2: Point, pp: Point) -> Optional[float]:
    """``f = sqrt(-(U-P).(V-P))``, or ``None`` if the pair cannot be perpendicular rays.

    ``None`` rather than a NaN, and it is not a failure to swallow: a non-negative dot
    product means the two vanishing points fall on the SAME side of the principal point,
    which no pair of perpendicular world directions can do. It is the cheapest possible
    test that a VP2 candidate is geometrically admissible, and the calibrator's search
    leans on exactly that.
    """
    d = (vp1[0] - pp[0]) * (vp2[0] - pp[0]) + (vp1[1] - pp[1]) * (vp2[1] - pp[1])
    if d >= 0.0:
        return None
    f = sqrt(-d)
    return f if isfinite(f) and f > 0.0 else None


def road_normal(vp1: Point, vp2: Point, pp: Point, focal: float) -> Vec3:
    """Unit normal of the road plane, in camera coordinates.

    The vertical vanishing direction is perpendicular to both road directions, so it is
    their cross product -- and the vertical direction of a road IS that road's normal.

    A vanishing point cannot tell a direction from its opposite, so the cross product
    arrives with an arbitrary sign. It is oriented against a pixel that is certainly
    road: low in the frame, well below the horizon. Get this wrong and every ray meets
    the plane BEHIND the camera, so :meth:`RoadPlane.project` returns ``None`` for the
    entire image -- a silent, total failure rather than a wrong number.
    """
    u = (vp1[0] - pp[0], vp1[1] - pp[1], focal)
    v = (vp2[0] - pp[0], vp2[1] - pp[1], focal)
    n = _unit(_cross(u, v))
    probe = (0.0, pp[1], focal)
    return n if _dot(probe, n) > 0.0 else (-n[0], -n[1], -n[2])


class CalibrationQuality:
    """What a vanishing-point pair is worth, before anything is measured with it.

    Two numbers, both cheap, and between them the difference between a speed and a
    plausible-looking fiction:

    ``vp2_distance_px``
        How far VP2 sits from the principal point. Past roughly 20 image diagonals it is
        an ideal point in all but name, and the focal length drawn from it is noise.

    ``f_sensitivity_pct``
        Since ``f^2 = -(U-P).(V-P)``, one pixel of error in VP1 moves ``f`` by
        ``|V-P| / (2 f^2)``. As a percentage this is the honest error bar on every speed
        that follows, because speed is linear in ``f``.

    ``ok`` is the conjunction. ``reason`` is empty exactly when ``ok`` is true, and is
    written for whoever has to fix the camera rather than for whoever wrote this.
    """

    def __init__(
        self,
        focal: Optional[float],
        vp2_distance_px: float,
        diagonal_px: float,
        max_vp2_diagonals: float,
        max_f_sensitivity_pct: float,
    ) -> None:
        self.focal = focal
        self.vp2_distance_px = vp2_distance_px
        self.diagonals = vp2_distance_px / diagonal_px if diagonal_px > 0.0 else float("inf")
        if focal is None:
            self.f_sensitivity_pct = float("inf")
            self.reason = (
                "vp1 and vp2 give no real focal length: they fall on the same side of "
                "the principal point, which two perpendicular directions cannot do. One "
                "of the two vanishing points is wrong -- most often vp2's sign, which is "
                "the least reliable thing about a vanishing point near infinity."
            )
        elif self.diagonals > max_vp2_diagonals:
            self.f_sensitivity_pct = 100.0 * vp2_distance_px / (2.0 * focal * focal)
            self.reason = (
                f"vp2 is {vp2_distance_px:.0f} px from the principal point "
                f"({self.diagonals:.1f} image diagonals, limit {max_vp2_diagonals}): "
                "degenerate. This camera looks too nearly along the road for the "
                "across-road direction to be measurable, so no focal length drawn from "
                "it means anything."
            )
        else:
            self.f_sensitivity_pct = 100.0 * vp2_distance_px / (2.0 * focal * focal)
            if self.f_sensitivity_pct > max_f_sensitivity_pct:
                self.reason = (
                    f"the focal length moves {self.f_sensitivity_pct:.1f} % per pixel of "
                    f"vp1 error (limit {max_f_sensitivity_pct} %): vp2 is too weak to "
                    "calibrate from. Every speed would inherit that sensitivity, because "
                    "speed is linear in the focal length."
                )
            else:
                self.reason = ""
        self.ok = not self.reason


def assess(
    vp1: Point,
    vp2: Point,
    pp: Point,
    width: float,
    height: float,
    max_vp2_diagonals: float = DEFAULT_MAX_VP2_DIAGONALS,
    max_f_sensitivity_pct: float = DEFAULT_MAX_F_SENSITIVITY_PCT,
) -> CalibrationQuality:
    """Grade a vanishing-point pair. Nothing here measures anything; it only judges."""
    return CalibrationQuality(
        focal_from_vps(vp1, vp2, pp),
        hypot(vp2[0] - pp[0], vp2[1] - pp[1]),
        hypot(width, height),
        max_vp2_diagonals,
        max_f_sensitivity_pct,
    )


class RoadPlane:
    """Maps a pixel to a point on the road, in metres, and measures distance along it.

    The plane is ``n.X = 1`` in camera coordinates. A pixel ``q`` becomes the ray
    ``qhat = (qx - px, qy - py, f)``; where that ray meets the plane is
    ``qhat / (n . qhat)``, and multiplying by ``lam`` turns road units into metres --
    ``lam`` being exactly the camera's perpendicular height above the road surface.

    The in-plane basis is oriented so ``e1`` runs ALONG the traffic direction (towards
    VP1) and ``e2`` across it. That split is not cosmetic: speed is the rate of change of
    the ``e1`` coordinate, and keeping the two axes named means a lateral wobble cannot
    be mistaken for forward motion.
    """

    def __init__(self, pp: Point, focal: float, vp1: Point, vp2: Point, lam: float) -> None:
        self.pp = pp
        self.f = focal
        self.lam = lam
        self.n = road_normal(vp1, vp2, pp, focal)

        d1 = (vp1[0] - pp[0], vp1[1] - pp[1], focal)
        d1 = _sub(d1, _scale(self.n, _dot(d1, self.n)))
        self.e1 = _unit(d1) if _norm(d1) > 1e-9 else (1.0, 0.0, 0.0)
        self.e2 = _unit(_cross(self.n, self.e1))

    def project(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        """Pixel -> ``(along, across)`` on the road in METRES, or ``None`` above the horizon.

        ``None`` is a real answer, not an error: a box whose bottom edge sits at or above
        the horizon has no intersection with the road ahead of the camera. In practice
        that is a bad detection, or a vehicle on a flyover. Returning a distance there
        would invent one, and it would be a large one.
        """
        q = (x - self.pp[0], y - self.pp[1], self.f)
        den = _dot(q, self.n)
        if den <= 1e-9:
            return None
        pt = _scale(q, self.lam / den)
        return _dot(pt, self.e1), _dot(pt, self.e2)

    def metres_per_pixel(self, x: float, y: float, pixels: float) -> float:
        """Ground metres spanned by ``pixels`` of vertical wobble at this image point.

        Vertical because foot-point noise is dominated by the box's bottom edge, and
        because the ground scale changes far faster down the image than across it.
        """
        here = self.project(x, y)
        there = self.project(x, y + pixels)
        if here is None or there is None:
            return 0.0
        return hypot(there[0] - here[0], there[1] - here[1])

    def horizon_y(self, x: float) -> Optional[float]:
        """Image row where the road plane vanishes, at image column ``x``."""
        if abs(self.n[1]) < 1e-12:
            return None
        return self.pp[1] - (self.n[0] * (x - self.pp[0]) + self.n[2] * self.f) / self.n[1]


def _dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _scale(a: Vec3, k: float) -> Vec3:
    return (a[0] * k, a[1] * k, a[2] * k)


def _cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _norm(a: Vec3) -> float:
    return sqrt(_dot(a, a))


def _unit(a: Vec3) -> Vec3:
    n = _norm(a)
    return (a[0] / n, a[1] / n, a[2] / n) if n > 1e-12 else (0.0, 0.0, 1.0)
