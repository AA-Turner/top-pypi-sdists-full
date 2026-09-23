"""Auto-generated stub for module: speed_fit_utils."""
from typing import Any, List, Optional, Tuple

from .speed_geometry_utils import RoadPlane

# Functions
def baseline_slope(window: List[List[float]], min_seconds: float) -> Optional[float]:
    """
    Median along-road speed, in metres per second, over long-enough baselines.
    """
    ...
def over_limit_pct(measured: float, limit: float) -> float:
    """
    How far above the posted limit, as a percentage. ``0.0`` when at or under.
    """
    ...
def severity_for(over_pct: float) -> str:
    """
    Grade an overage. Round numbers: a starting policy, not a measurement.
    """
    ...
def uncertainty_pct(window: List[List[float]], pixel: Tuple[float, float], plane: Any, jitter_px: float) -> float:
    """
    Foot-point jitter as a percentage of the baseline the speed was fitted over.
    
        Converted to ground metres at this vehicle's own pixel, because the same wobble is
        worth far more ground near the horizon than near the camera. Two endpoints each carry
        it, so it enters the difference 1.414x.
    
        Deliberately excludes any scale term: a wrong ``camera_height_m`` biases every reading
        in the deployment equally, and folding a guess at it in here would imply the two
        errors are the same kind. They are not -- this one shrinks as the baseline grows and
        that one never shrinks at all.
    """
    ...
