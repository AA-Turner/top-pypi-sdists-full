"""FortiOS CMDB - Ddns category"""

from .lookup import Lookup
from .servers import Servers

__all__ = [
    "Ddns",
    "Lookup",
    "Servers",
]


class Ddns:
    """Ddns endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ddns endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.lookup = Lookup(client)
        self.servers = Servers(client)
