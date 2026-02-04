"""FortiOS CMDB - Dhcp6 category"""

from .server import Server

__all__ = [
    "Dhcp6",
    "Server",
]


class Dhcp6:
    """Dhcp6 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dhcp6 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.server = Server(client)
