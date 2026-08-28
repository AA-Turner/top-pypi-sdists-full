"""License Plate Recognition — Access Control profile (barrier / gate mounted camera)."""

from dataclasses import dataclass

from .license_plate_monitoring import (
    LicensePlateMonitorConfig,
    LicensePlateMonitorUseCase,
)


@dataclass
class LicensePlateAccessControlConfig(LicensePlateMonitorConfig):
    """Precision-first gates for a vehicle stopped at a barrier.

    A wrong read here opens a gate for the wrong vehicle, so every gate is raised
    relative to the base profile. A missed read costs almost nothing: the vehicle
    is stationary and the next frame gets another attempt.

    ``confidence_threshold`` is intentionally left at the base value -- ``process``
    overwrites it with a literal 0.37 on every call, so setting it here would be
    silently discarded. See ``_apply_profile_gates``.
    """

    usecase: str = "lpr_access_control"
    category: str = "license_plate_monitor"

    # Demand three agreeing OCR samples instead of one. This is the single
    # biggest precision gain available: the vehicle is stationary, so frames are
    # cheap, and one confused character no longer decides an access event.
    stable_frames_required: int = 3
    ocr_confidence_threshold: float = 0.85
    min_plate_len: int = 5  # a 3-char read at a barrier is a partial read

    # A stationary vehicle does not need occlusion carry, and a tighter IoU keeps
    # a neighbouring vehicle's plate from being associated to this track.
    smoother_hold_frames: int = 2
    smoother_iou_threshold: float = 0.4

    # One vehicle presentation should produce one access event, not a stream of
    # view frames -- the base 60 s floor is aimed at CCTV write volume.
    plate_log_min_interval_s: float = 300.0
    lpr_max_frame_age_s: float = 3.0  # a stale gate event is worthless


class LicensePlateAccessControlUseCase(LicensePlateMonitorUseCase):
    """Access-control LPR: stationary vehicle, stricter confirmation."""

    def __init__(self):
        super().__init__()
        self.name = "lpr_access_control"
        self.category = "license_plate_monitor"
        self.CASE_TYPE = "lpr_access_control"
        self.CASE_VERSION = "1.0"
