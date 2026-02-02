"""FortiOS CMDB - Acl6 category"""

from ..acl6_base import Acl6 as Acl6Base
from .clear_counters import ClearCounters

__all__ = [
    "Acl6",
    "ClearCounters",
]


class Acl6(Acl6Base):
    """Acl6 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Acl6 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
