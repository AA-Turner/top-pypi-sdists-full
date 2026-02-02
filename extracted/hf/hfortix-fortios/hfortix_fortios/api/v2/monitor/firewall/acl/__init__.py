"""FortiOS CMDB - Acl category"""

from ..acl_base import Acl as AclBase
from .clear_counters import ClearCounters

__all__ = [
    "Acl",
    "ClearCounters",
]


class Acl(AclBase):
    """Acl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Acl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
