"""FortiOS CMDB - MaliciousUrls category"""

from ..malicious_urls_base import MaliciousUrls as MaliciousUrlsBase
from .stat import Stat

__all__ = [
    "MaliciousUrls",
    "Stat",
]


class MaliciousUrls(MaliciousUrlsBase):
    """MaliciousUrls endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """MaliciousUrls endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.stat = Stat(client)
