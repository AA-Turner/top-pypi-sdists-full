"""FortiOS CMDB - VlanProbe category (stub)"""

from typing import Any
from ..vlan_probe_base import VlanProbe as VlanProbeBase
from .start import Start
from .stop import Stop

class VlanProbe(VlanProbeBase):
    """VlanProbe endpoints wrapper for CMDB API."""

    start: Start
    stop: Stop

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
