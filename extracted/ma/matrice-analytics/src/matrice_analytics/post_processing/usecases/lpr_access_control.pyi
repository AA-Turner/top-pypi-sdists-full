"""Auto-generated stub for module: lpr_access_control."""
from typing import Any

from .license_plate_monitoring import LicensePlateMonitorConfig, LicensePlateMonitorUseCase

# Classes
class LicensePlateAccessControlConfig:
    # Precision-first gates for a vehicle stopped at a barrier.
    #
    #     A wrong read here opens a gate for the wrong vehicle, so every gate is raised
    #     relative to the base profile. A missed read costs almost nothing: the vehicle
    #     is stationary and the next frame gets another attempt.
    #
    #     ``confidence_threshold`` is intentionally left at the base value -- ``process``
    #     overwrites it with a literal 0.37 on every call, so setting it here would be
    #     silently discarded. See ``_apply_profile_gates``.

    ...
class LicensePlateAccessControlUseCase:
    # Access-control LPR: stationary vehicle, stricter confirmation.

    def __init__(self: Any) -> None: ...

