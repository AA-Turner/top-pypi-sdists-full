"""Reading a speed off one vehicle's trajectory, and grading how far over the limit.

Split out of the use case module so it stays inside the org file-size cap. These are pure
functions over a trajectory -- no state, no config object, no engine types -- which also
makes them the part that is straightforward to test on its own.
"""

from statistics import median
from typing import List, Optional, Tuple

from .speed_geometry_utils import RoadPlane


def baseline_slope(window: List[List[float]], min_seconds: float) -> Optional[float]:
    """Median along-road speed, in metres per second, over long-enough baselines."""
    t_now, a_now = window[-1][0], window[-1][1]
    slopes = [(a_now - a) / (t_now - t) for t, a, _ in window[:-1] if t_now - t >= min_seconds]
    return median(slopes) if slopes else None


def uncertainty_pct(
    window: List[List[float]],
    pixel: Tuple[float, float],
    plane: RoadPlane,
    jitter_px: float,
) -> float:
    """Foot-point jitter as a percentage of the baseline the speed was fitted over.

    Converted to ground metres at this vehicle's own pixel, because the same wobble is
    worth far more ground near the horizon than near the camera. Two endpoints each carry
    it, so it enters the difference 1.414x.

    Deliberately excludes any scale term: a wrong ``camera_height_m`` biases every reading
    in the deployment equally, and folding a guess at it in here would imply the two
    errors are the same kind. They are not -- this one shrinks as the baseline grows and
    that one never shrinks at all.
    """
    span = abs(window[-1][1] - window[0][1])
    if span <= 0.0:
        return 100.0
    jitter_m = float(plane.metres_per_pixel(pixel[0], pixel[1], jitter_px))
    if jitter_m <= 0.0:
        return 0.0
    return round(min(100.0, 100.0 * 1.414 * jitter_m / span), 1)


def over_limit_pct(measured: float, limit: float) -> float:
    """How far above the posted limit, as a percentage. ``0.0`` when at or under."""
    if limit <= 0.0 or measured <= limit:
        return 0.0
    return ((measured - limit) / limit) * 100.0


def severity_for(over_pct: float) -> str:
    """Grade an overage. Round numbers: a starting policy, not a measurement."""
    if over_pct >= 100.0:
        return "critical"
    if over_pct >= 50.0:
        return "high"
    if over_pct >= 25.0:
        return "medium"
    return "low"
