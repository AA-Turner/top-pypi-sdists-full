"""FortiOS CMDB - Lookup category"""

from ..lookup_base import Lookup as LookupBase
from .ha_peer import HaPeer

__all__ = [
    "HaPeer",
    "Lookup",
]


class Lookup(LookupBase):
    """Lookup endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Lookup endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.ha_peer = HaPeer(client)
