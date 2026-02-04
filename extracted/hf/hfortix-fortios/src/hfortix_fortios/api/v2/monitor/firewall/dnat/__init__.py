"""FortiOS CMDB - Dnat category"""

from ..dnat_base import Dnat as DnatBase
from .clear_counters import ClearCounters
from .reset import Reset

__all__ = [
    "ClearCounters",
    "Dnat",
    "Reset",
]


class Dnat(DnatBase):
    """Dnat endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dnat endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
        self.reset = Reset(client)
