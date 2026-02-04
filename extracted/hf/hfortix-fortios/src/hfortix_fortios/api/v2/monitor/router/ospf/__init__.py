"""FortiOS CMDB - Ospf category"""

from .neighbors import Neighbors

__all__ = [
    "Neighbors",
    "Ospf",
]


class Ospf:
    """Ospf endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ospf endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.neighbors = Neighbors(client)
