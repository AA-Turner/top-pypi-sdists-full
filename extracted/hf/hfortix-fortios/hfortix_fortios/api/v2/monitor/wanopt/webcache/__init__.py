"""FortiOS CMDB - Webcache category"""

from ..webcache_base import Webcache as WebcacheBase
from .reset import Reset

__all__ = [
    "Reset",
    "Webcache",
]


class Webcache(WebcacheBase):
    """Webcache endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Webcache endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
