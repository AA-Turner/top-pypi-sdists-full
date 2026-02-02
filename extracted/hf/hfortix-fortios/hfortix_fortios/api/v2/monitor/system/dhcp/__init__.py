"""FortiOS CMDB - Dhcp category"""

from ..dhcp_base import Dhcp as DhcpBase
from .revoke import Revoke

__all__ = [
    "Dhcp",
    "Revoke",
]


class Dhcp(DhcpBase):
    """Dhcp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dhcp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.revoke = Revoke(client)
