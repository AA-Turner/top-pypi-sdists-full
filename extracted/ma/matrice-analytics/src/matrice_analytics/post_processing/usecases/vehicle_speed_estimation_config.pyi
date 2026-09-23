"""Auto-generated stub for module: vehicle_speed_estimation_config."""
from typing import Any, Dict, List, Optional

from ..core.config import BaseConfig

# Constants
FACTORS: Dict[Any, Any]
UNIT_LABELS: Dict[Any, Any]
VEHICLE_CATEGORIES: List[Any]

# Classes
class VehicleSpeedEstimationConfig:
    # Configuration for self-calibrating vehicle speed estimation.

    def __init__(self: Any, usecase: str = 'vehicle_speed_estimation', category: str = 'traffic', confidence_threshold: float = 0.5, target_categories: Optional[List[str]] = None, camera_height_m: float = 8.0, speed_limit: float = 50.0, units: str = 'kmh', tolerance: float = 0.1, window_samples: int = 40, min_samples: int = 12, min_baseline_seconds: float = 0.4, max_plausible_speed: float = 200.0, edge_margin_px: float = 6.0, jitter_px: float = 2.0, calibration_min_frames: int = 150, calibration_min_tracks: int = 25, calibration_retry_frames: int = 300, calibration_max_attempts: int = 5, max_vp2_diagonals: float = 20.0, max_f_sensitivity_pct: float = 2.0, **kwargs: Any) -> None: ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Serialise every field, not only the ones ``BaseConfig`` declares.
        
                ``BaseConfig.to_dict`` walks ``dataclasses.fields(self)``. This class is a plain
                class, not a dataclass, so without this override the config template and every
                dict round-trip would silently drop every field below.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration.
        """
        ...

