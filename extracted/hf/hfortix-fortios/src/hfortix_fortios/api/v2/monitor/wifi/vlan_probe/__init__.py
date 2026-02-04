"""FortiOS CMDB - VlanProbe category"""

from ..vlan_probe_base import VlanProbe as VlanProbeBase
from .start import Start
from .stop import Stop

__all__ = [
    "Start",
    "Stop",
    "VlanProbe",
]


class VlanProbe(VlanProbeBase):
    """VlanProbe endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """VlanProbe endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.start = Start(client)
        self.stop = Stop(client)
