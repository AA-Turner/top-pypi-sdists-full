"""Auto-generated stub for module: lpr_surveillance."""
from typing import Any

from .license_plate_monitoring import LicensePlateMonitorConfig, LicensePlateMonitorUseCase

# Classes
class LicensePlateSurveillanceConfig:
    # Recall-first gates for small, distant, motion-blurred plates.
    #
    #     Mirror image of the access-control profile: here a missed plate is gone for
    #     good (the vehicle has driven past), while a mis-logged sighting is cheap and
    #     correctable. Close to the legacy base behaviour, loosened where the base was
    #     tuned for a cleaner scene than a road.

    ...
class LicensePlateSurveillanceUseCase:
    # Surveillance LPR: many plates, tolerant gates, longer occlusion carry.

    def __init__(self: Any) -> None: ...

