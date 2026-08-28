"""License Plate Recognition — Surveillance profile (road / forecourt CCTV)."""

from dataclasses import dataclass

from .license_plate_monitoring import (
    LicensePlateMonitorConfig,
    LicensePlateMonitorUseCase,
)


@dataclass
class LicensePlateSurveillanceConfig(LicensePlateMonitorConfig):
    """Recall-first gates for small, distant, motion-blurred plates.

    Mirror image of the access-control profile: here a missed plate is gone for
    good (the vehicle has driven past), while a mis-logged sighting is cheap and
    correctable. Close to the legacy base behaviour, loosened where the base was
    tuned for a cleaner scene than a road.
    """

    usecase: str = "lpr_surveillance"
    category: str = "license_plate_monitor"

    stable_frames_required: int = 1  # a fast vehicle may only be readable once
    ocr_confidence_threshold: float = 0.65
    min_plate_len: int = 3

    # Vehicles occlude each other constantly at an angle, so carry a dropped
    # detection further before giving up on the track.
    enable_smoothing: bool = True
    smoother_hold_frames: int = 6
    smoother_iou_threshold: float = 0.3

    # Write volume is the binding constraint on a busy road -- keep the 60 s
    # per-plate coalescing floor that the base profile established.
    plate_log_min_interval_s: float = 60.0


class LicensePlateSurveillanceUseCase(LicensePlateMonitorUseCase):
    """Surveillance LPR: many plates, tolerant gates, longer occlusion carry."""

    def __init__(self):
        super().__init__()
        self.name = "lpr_surveillance"
        self.category = "license_plate_monitor"
        self.CASE_TYPE = "lpr_surveillance"
        self.CASE_VERSION = "1.0"
