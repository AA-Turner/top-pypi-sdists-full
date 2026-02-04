"""FortiOS CMDB - Forticloud category"""

from ..forticloud_base import Forticloud as ForticloudBase
from .connection import Connection

__all__ = [
    "Connection",
    "Forticloud",
]


class Forticloud(ForticloudBase):
    """Forticloud endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Forticloud endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.connection = Connection(client)
