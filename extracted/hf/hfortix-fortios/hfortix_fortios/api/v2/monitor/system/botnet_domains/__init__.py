"""FortiOS CMDB - BotnetDomains category"""

from ..botnet_domains_base import BotnetDomains as BotnetDomainsBase
from .hits import Hits
from .stat import Stat

__all__ = [
    "BotnetDomains",
    "Hits",
    "Stat",
]


class BotnetDomains(BotnetDomainsBase):
    """BotnetDomains endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """BotnetDomains endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.hits = Hits(client)
        self.stat = Stat(client)
