"""Configuration for the self-calibrating vehicle speed estimation use case.

Its own module for the same reason the calibrator is split in two: the use case file is
over the org size cap otherwise. It is also the half an installer actually reads, and the
half whose every field carries the reason its default is what it is.
"""

from typing import Any, Dict, List, Optional

from ..core.config import BaseConfig

#: m/s -> the configured unit, and the label that goes with it. ONE table, so a
#: deployment cannot convert in km/h and label in mph: both are read from the same key.
FACTORS = {"kmh": 3.6, "mph": 2.236936}
UNIT_LABELS = {"kmh": "km/h", "mph": "mph"}

VEHICLE_CATEGORIES = ["car", "truck", "bus", "motorcycle"]


class VehicleSpeedEstimationConfig(BaseConfig):
    """Configuration for self-calibrating vehicle speed estimation."""

    def __init__(
        self,
        usecase: str = "vehicle_speed_estimation",
        category: str = "traffic",
        confidence_threshold: float = 0.5,
        target_categories: Optional[List[str]] = None,
        camera_height_m: float = 8.0,
        speed_limit: float = 50.0,
        units: str = "kmh",
        tolerance: float = 0.1,
        window_samples: int = 40,
        min_samples: int = 12,
        min_baseline_seconds: float = 0.4,
        max_plausible_speed: float = 200.0,
        edge_margin_px: float = 6.0,
        jitter_px: float = 2.0,
        calibration_min_frames: int = 150,
        calibration_min_tracks: int = 25,
        calibration_retry_frames: int = 300,
        calibration_max_attempts: int = 5,
        max_vp2_diagonals: float = 20.0,
        max_f_sensitivity_pct: float = 2.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(usecase=usecase, category=category, **kwargs)
        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or list(VEHICLE_CATEGORIES)
        #: The only real-world measurement this use case asks for. Every speed is exactly
        #: linear in it.
        self.camera_height_m = camera_height_m
        self.speed_limit = speed_limit
        self.units = units
        #: Fractional hysteresis above the limit before a vehicle is flagged. The offender
        #: set never un-counts, so a vehicle flickering across the threshold would be
        #: counted once and stay counted.
        self.tolerance = tolerance
        self.window_samples = window_samples
        self.min_samples = min_samples
        self.min_baseline_seconds = min_baseline_seconds
        self.max_plausible_speed = max_plausible_speed
        self.edge_margin_px = edge_margin_px
        self.jitter_px = jitter_px
        self.calibration_min_frames = calibration_min_frames
        self.calibration_min_tracks = calibration_min_tracks
        self.calibration_retry_frames = calibration_retry_frames
        self.calibration_max_attempts = calibration_max_attempts
        self.max_vp2_diagonals = max_vp2_diagonals
        self.max_f_sensitivity_pct = max_f_sensitivity_pct

    def to_dict(self) -> Dict[str, Any]:
        """Serialise every field, not only the ones ``BaseConfig`` declares.

        ``BaseConfig.to_dict`` walks ``dataclasses.fields(self)``. This class is a plain
        class, not a dataclass, so without this override the config template and every
        dict round-trip would silently drop every field below.
        """
        data = super().to_dict()
        for key, value in vars(self).items():
            if key in data or value is None:
                continue
            data[key] = value.to_dict() if hasattr(value, "to_dict") else value
        return data

    def validate(self) -> List[str]:
        """Validate configuration."""
        errors = super().validate()
        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0.0 and 1.0")
        if self.camera_height_m <= 0.0:
            errors.append("camera_height_m must be positive: it is the camera's height in metres")
        if self.speed_limit <= 0.0:
            errors.append("speed_limit must be positive")
        if self.units not in FACTORS:
            errors.append(f"units must be one of {sorted(FACTORS)}")
        if self.tolerance < 0.0:
            errors.append("tolerance must not be negative")
        if self.min_samples < 2:
            errors.append("min_samples must be at least 2: a slope needs two points")
        if self.window_samples < self.min_samples:
            errors.append("window_samples must be at least min_samples")
        if self.min_baseline_seconds <= 0.0:
            errors.append("min_baseline_seconds must be positive")
        if self.max_plausible_speed <= 0.0:
            errors.append("max_plausible_speed must be positive")
        return errors


#: Config schema advertised to the platform.
VEHICLE_SPEED_ESTIMATION_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "camera_height_m": {
            "type": "number",
            "minimum": 0.1,
            "default": 8.0,
            "description": (
                "Perpendicular height of the camera above the road surface, in "
                "metres. The only real-world measurement this use case needs; "
                "every speed is exactly linear in it."
            ),
        },
        "speed_limit": {
            "type": "number",
            "minimum": 0.1,
            "default": 50.0,
            "description": "Posted speed limit, in `units`.",
        },
        "units": {
            "type": "string",
            "enum": ["kmh", "mph"],
            "default": "kmh",
            "description": "Drives both the conversion and the reported label.",
        },
        "tolerance": {
            "type": "number",
            "minimum": 0.0,
            "default": 0.1,
            "description": "Fractional hysteresis above the limit before flagging.",
        },
        "confidence_threshold": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0,
            "default": 0.5,
            "description": "Minimum detection confidence. Every box is a position.",
        },
        "calibration_min_frames": {
            "type": "integer",
            "minimum": 1,
            "default": 150,
            "description": "Frames of background to gather before calibrating.",
        },
        "calibration_min_tracks": {
            "type": "integer",
            "minimum": 1,
            "default": 25,
            "description": "Vehicle tracks needed before the traffic direction is fitted.",
        },
    },
}

# ------------------------------------------------------------------ frame
