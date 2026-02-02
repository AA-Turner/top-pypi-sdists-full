"""FortiOS CMDB - MulticastPolicy6 category"""

from ..multicast_policy6_base import MulticastPolicy6 as MulticastPolicy6Base
from .clear_counters import ClearCounters
from .reset import Reset

__all__ = [
    "ClearCounters",
    "MulticastPolicy6",
    "Reset",
]


class MulticastPolicy6(MulticastPolicy6Base):
    """MulticastPolicy6 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """MulticastPolicy6 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
        self.reset = Reset(client)
