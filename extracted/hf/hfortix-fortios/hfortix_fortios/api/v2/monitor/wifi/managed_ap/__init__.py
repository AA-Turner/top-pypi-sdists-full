"""FortiOS CMDB - ManagedAp category"""

from ..managed_ap_base import ManagedAp as ManagedApBase
from .led_blink import LedBlink
from .restart import Restart
from .set_status import SetStatus

__all__ = [
    "LedBlink",
    "ManagedAp",
    "Restart",
    "SetStatus",
]


class ManagedAp(ManagedApBase):
    """ManagedAp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ManagedAp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.led_blink = LedBlink(client)
        self.restart = Restart(client)
        self.set_status = SetStatus(client)
