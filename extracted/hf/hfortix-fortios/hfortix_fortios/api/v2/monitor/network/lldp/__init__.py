"""FortiOS CMDB - Lldp category"""

from .neighbors import Neighbors
from .ports import Ports

__all__ = [
    "Lldp",
    "Neighbors",
    "Ports",
]


class Lldp:
    """Lldp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Lldp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.neighbors = Neighbors(client)
        self.ports = Ports(client)
