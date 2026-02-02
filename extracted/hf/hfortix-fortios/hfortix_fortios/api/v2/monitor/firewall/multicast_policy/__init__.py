"""FortiOS CMDB - MulticastPolicy category"""

from ..multicast_policy_base import MulticastPolicy as MulticastPolicyBase
from .clear_counters import ClearCounters
from .reset import Reset

__all__ = [
    "ClearCounters",
    "MulticastPolicy",
    "Reset",
]


class MulticastPolicy(MulticastPolicyBase):
    """MulticastPolicy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """MulticastPolicy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
        self.reset = Reset(client)
