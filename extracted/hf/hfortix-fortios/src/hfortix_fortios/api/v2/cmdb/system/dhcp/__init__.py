"""FortiOS CMDB - Dhcp category"""

from .server import Server

__all__ = [
    "Dhcp",
    "Server",
]


class Dhcp:
    """Dhcp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dhcp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.server = Server(client)
