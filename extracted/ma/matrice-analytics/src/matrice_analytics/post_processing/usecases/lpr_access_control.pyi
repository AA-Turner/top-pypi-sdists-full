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
    #     ``confidence_threshold`` is configurable per deployment and is no longer overwritten
    #     by ``process``. This profile leaves the dataclass default alone deliberately: the gate
    #     belongs in the deployment config next to the camera it was tuned against, not baked
    #     into the class.

    ...
class LicensePlateAccessControlUseCase:
    # Access-control LPR: stationary vehicle, stricter confirmation.

    def __init__(self: Any) -> None: ...

