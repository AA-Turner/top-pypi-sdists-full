from typing import Optional

from dlt.common.configuration.resolve import resolve_configuration
from dlt.common.configuration.specs import RuntimeConfiguration
from dlt.common.runtime.anon_tracker import get_anonymous_id

DEVICE_ID_HEADER = "x-dlt-device-id"


def get_telemetry_device_id() -> Optional[str]:
    """dlt's anonymous device id, or None when the user opted out of telemetry."""
    try:
        if not resolve_configuration(RuntimeConfiguration()).dlthub_telemetry:
            return None
        return get_anonymous_id().strip() or None
    except Exception:
        return None
