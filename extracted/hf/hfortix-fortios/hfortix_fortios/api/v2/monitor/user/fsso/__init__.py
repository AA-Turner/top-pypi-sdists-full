"""FortiOS CMDB - Fsso category"""

from ..fsso_base import Fsso as FssoBase
from .refresh_server import RefreshServer

__all__ = [
    "Fsso",
    "RefreshServer",
]


class Fsso(FssoBase):
    """Fsso endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fsso endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.refresh_server = RefreshServer(client)
