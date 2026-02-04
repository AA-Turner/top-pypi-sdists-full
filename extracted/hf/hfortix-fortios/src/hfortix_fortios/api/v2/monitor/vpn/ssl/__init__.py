"""FortiOS CMDB - Ssl category"""

from ..ssl_base import Ssl as SslBase
from .clear_tunnel import ClearTunnel
from .delete import Delete
from .stats import Stats

__all__ = [
    "ClearTunnel",
    "Delete",
    "Ssl",
    "Stats",
]


class Ssl(SslBase):
    """Ssl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ssl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_tunnel = ClearTunnel(client)
        self.delete = Delete(client)
        self.stats = Stats(client)
