"""FortiOS CMDB - Firewall category"""

from ..firewall_base import Firewall as FirewallBase
from .auth import Auth
from .count import Count
from .deauth import Deauth

__all__ = [
    "Auth",
    "Count",
    "Deauth",
    "Firewall",
]


class Firewall(FirewallBase):
    """Firewall endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Firewall endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.auth = Auth(client)
        self.count = Count(client)
        self.deauth = Deauth(client)
