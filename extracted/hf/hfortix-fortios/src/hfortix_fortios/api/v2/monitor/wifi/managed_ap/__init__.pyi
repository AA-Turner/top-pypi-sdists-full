"""FortiOS CMDB - ManagedAp category (stub)"""

from typing import Any
from ..managed_ap_base import ManagedAp as ManagedApBase
from .led_blink import LedBlink
from .restart import Restart
from .set_status import SetStatus

class ManagedAp(ManagedApBase):
    """ManagedAp endpoints wrapper for CMDB API."""

    led_blink: LedBlink
    restart: Restart
    set_status: SetStatus

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
