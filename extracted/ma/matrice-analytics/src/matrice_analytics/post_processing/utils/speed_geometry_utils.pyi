"""Auto-generated stub for module: speed_geometry_utils."""
from typing import Any, Optional, Tuple

# Constants
DEFAULT_MAX_F_SENSITIVITY_PCT: float
DEFAULT_MAX_VP2_DIAGONALS: float
Point: Any
Vec3: Any

# Functions
def assess(vp1: Any, vp2: Any, pp: Any, width: float, height: float, max_vp2_diagonals: float = DEFAULT_MAX_VP2_DIAGONALS, max_f_sensitivity_pct: float = DEFAULT_MAX_F_SENSITIVITY_PCT) -> Any:
    """
    Grade a vanishing-point pair. Nothing here measures anything; it only judges.
    """
    ...
def focal_from_vps(vp1: Any, vp2: Any, pp: Any) -> Optional[float]:
    """
    ``f = sqrt(-(U-P).(V-P))``, or ``None`` if the pair cannot be perpendicular rays.
    
        ``None`` rather than a NaN, and it is not a failure to swallow: a non-negative dot
        product means the two vanishing points fall on the SAME side of the principal point,
        which no pair of perpendicular world directions can do. It is the cheapest possible
        test that a VP2 candidate is geometrically admissible, and the calibrator's search
        leans on exactly that.
    """
    ...
def road_normal(vp1: Any, vp2: Any, pp: Any, focal: float) -> Any:
    """
    Unit normal of the road plane, in camera coordinates.
    
        The vertical vanishing direction is perpendicular to both road directions, so it is
        their cross product -- and the vertical direction of a road IS that road's normal.
    
        A vanishing point cannot tell a direction from its opposite, so the cross product
        arrives with an arbitrary sign. It is oriented against a pixel that is certainly
        road: low in the frame, well below the horizon. Get this wrong and every ray meets
        the plane BEHIND the camera, so :meth:`RoadPlane.project` returns ``None`` for the
        entire image -- a silent, total failure rather than a wrong number.
    """
    ...

# Classes
class CalibrationQuality:
    # What a vanishing-point pair is worth, before anything is measured with it.
    #
    #     Two numbers, both cheap, and between them the difference between a speed and a
    #     plausible-looking fiction:
    #
    #     ``vp2_distance_px``
    #         How far VP2 sits from the principal point. Past roughly 20 image diagonals it is
    #         an ideal point in all but name, and the focal length drawn from it is noise.
    #
    #     ``f_sensitivity_pct``
    #         Since ``f^2 = -(U-P).(V-P)``, one pixel of error in VP1 moves ``f`` by
    #         ``|V-P| / (2 f^2)``. As a percentage this is the honest error bar on every speed
    #         that follows, because speed is linear in ``f``.
    #
    #     ``ok`` is the conjunction. ``reason`` is empty exactly when ``ok`` is true, and is
    #     written for whoever has to fix the camera rather than for whoever wrote this.

    def __init__(self: Any, focal: Optional[float], vp2_distance_px: float, diagonal_px: float, max_vp2_diagonals: float, max_f_sensitivity_pct: float) -> None: ...

class RoadPlane:
    # Maps a pixel to a point on the road, in metres, and measures distance along it.
    #
    #     The plane is ``n.X = 1`` in camera coordinates. A pixel ``q`` becomes the ray
    #     ``qhat = (qx - px, qy - py, f)``; where that ray meets the plane is
    #     ``qhat / (n . qhat)``, and multiplying by ``lam`` turns road units into metres --
    #     ``lam`` being exactly the camera's perpendicular height above the road surface.
    #
    #     The in-plane basis is oriented so ``e1`` runs ALONG the traffic direction (towards
    #     VP1) and ``e2`` across it. That split is not cosmetic: speed is the rate of change of
    #     the ``e1`` coordinate, and keeping the two axes named means a lateral wobble cannot
    #     be mistaken for forward motion.

    def __init__(self: Any, pp: Any, focal: float, vp1: Any, vp2: Any, lam: float) -> None: ...

    def horizon_y(self: Any, x: float) -> Optional[float]:
        """
        Image row where the road plane vanishes, at image column ``x``.
        """
        ...

    def metres_per_pixel(self: Any, x: float, y: float, pixels: float) -> float:
        """
        Ground metres spanned by ``pixels`` of vertical wobble at this image point.
        
                Vertical because foot-point noise is dominated by the box's bottom edge, and
                because the ground scale changes far faster down the image than across it.
        """
        ...

    def project(self: Any, x: float, y: float) -> Optional[Tuple[float, float]]:
        """
        Pixel -> ``(along, across)`` on the road in METRES, or ``None`` above the horizon.
        
                ``None`` is a real answer, not an error: a box whose bottom edge sits at or above
                the horizon has no intersection with the road ahead of the camera. In practice
                that is a bad detection, or a vehicle on a flyover. Returning a distance there
                would invent one, and it would be a large one.
        """
        ...

