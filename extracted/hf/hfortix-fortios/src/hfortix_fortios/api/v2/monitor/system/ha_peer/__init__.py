"""FortiOS CMDB - HaPeer category"""

from ..ha_peer_base import HaPeer as HaPeerBase
from .disconnect import Disconnect
from .update import Update

__all__ = [
    "Disconnect",
    "HaPeer",
    "Update",
]


class HaPeer(HaPeerBase):
    """HaPeer endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """HaPeer endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.disconnect = Disconnect(client)
        self.update = Update(client)
