"""Auto-generated stub for module: speed_paint_calibration_utils."""
from typing import Any, Dict, List, Optional, Tuple

from .speed_geometry_utils import DEFAULT_MAX_F_SENSITIVITY_PCT, assess, focal_from_vps
from .speed_paint_utils import paint_mask, road_mask_from_points, segments_from_paint, split_by_vp1

# Constants
logger: Any

# Functions
def solve_vp2(segs: Any.Any, vp1: Any.Any, pp: Any.Any, iters: int = 20000) -> Optional[Tuple[Any.Any, Any.Any]]:
    """
    VP2 from the transverse segments, constrained to calibrate against VP1.
    
        Every candidate that does not yield a real focal length against VP1 is rejected
        outright -- that single test is what stops the fit landing on the wrong side of the
        principal point, which is where an unconstrained fit reliably goes.
    """
    ...
def track_chords(tracks: Dict[int, List[Tuple[float, float]]], min_points: int = 6, min_length_px: float = 40.0) -> Any.Any:
    """
    One chord per track: first observed ground point to last, in pixels.
    
        A chord rather than every consecutive pair. Consecutive points are a few pixels apart
        and their direction is mostly jitter; the chord of a whole track is a long baseline
        whose direction is the direction the vehicle actually travelled. Short tracks and
        short chords are dropped for the same reason -- they are id noise, and they vote.
    """
    ...
def vp2_on_horizon(segs: Any.Any, horizon_y: float, pp: Any.Any, vp1: Any.Any) -> Optional[Tuple[Any.Any, int]]:
    """
    VP2 constrained to the road's vanishing line. One free parameter, not two.
    
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
    ...
def vp_ransac(segs: Any.Any, angle_tol_deg: float = 2.0, iters: int = 20000, seed: int = 0) -> Tuple[Optional[Any.Any], Any.Any]:
    """
    Vanishing point of a family of segments. Returns ``(vp, inlier mask)``.
    
        Scored by the ANGLE between each segment and the direction from its midpoint to the
        candidate, never by point-line distance. For a vanishing point near infinity -- the
        normal case for a road receding from the camera -- distance is enormous for every
        candidate and carries no information, while the angle stays meaningful throughout.
    """
    ...

# Classes
class CalibrationResult:
    # The outcome of one calibration attempt: either a camera, or why there isn't one.

    def __init__(self: Any, vp1: Optional[Tuple[float, float]] = None, vp2: Optional[Tuple[float, float]] = None, focal: Optional[float] = None, reason: str = '', permanent: bool = False, diagnostics: Optional[Dict[str, float]] = None) -> None: ...

    def ok(self: Any) -> bool: ...

class SelfCalibrator:
    # Accumulates a background plate and vehicle tracks, then recovers the camera.
    #
    #     Deliberately stateful and per camera. It holds one background model and a bounded
    #     number of track chords, and nothing else -- no frames are retained, which is what
    #     makes it affordable to run one of these per stream.

    def __init__(self: Any, min_frames: int = 150, min_tracks: int = 25, max_tracks: int = 400, retry_interval_frames: int = 300, max_attempts: int = 5, tophat: int = 35, tophat_thresh: int = 22, roi_top: float = 0.3, min_len: int = 30, vp1_reject_deg: float = 12.0, max_vp2_diagonals: float = 20.0, max_f_sensitivity_pct: float = DEFAULT_MAX_F_SENSITIVITY_PCT) -> None: ...

    def attempt(self: Any, width: int, height: int) -> Any:
        """
        Try once to recover the camera. Expensive; call only when :meth:`ready`.
        """
        ...

    def done(self: Any) -> bool:
        """
        True once there is a camera, or once it is established there will not be one.
        """
        ...

    def observe_frame(self: Any, frame: Any.Any) -> None:
        """
        Feed one frame into the background model. Cheap; safe to call per frame.
        """
        ...

    def observe_track(self: Any, track_id: int, x: float, y: float) -> None:
        """
        Record one vehicle ground point, in pixels, for the VP1 fit.
        """
        ...

    def ready(self: Any) -> bool:
        """
        Is there enough evidence to be worth attempting a calibration?
        """
        ...

