"""FortiOS CMDB - CentralSnatMap category"""

from ..central_snat_map_base import CentralSnatMap as CentralSnatMapBase
from .clear_counters import ClearCounters
from .reset import Reset

__all__ = [
    "CentralSnatMap",
    "ClearCounters",
    "Reset",
]


class CentralSnatMap(CentralSnatMapBase):
    """CentralSnatMap endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """CentralSnatMap endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
        self.reset = Reset(client)
