"""FortiOS CMDB - Dhcp6 category"""

from .revoke import Revoke

__all__ = [
    "Dhcp6",
    "Revoke",
]


class Dhcp6:
    """Dhcp6 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dhcp6 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.revoke = Revoke(client)
