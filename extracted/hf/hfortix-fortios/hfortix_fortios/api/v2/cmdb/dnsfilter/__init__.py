"""FortiOS CMDB - Dnsfilter category"""

from .domain_filter import DomainFilter
from .profile import Profile

__all__ = [
    "Dnsfilter",
    "DomainFilter",
    "Profile",
]


class Dnsfilter:
    """Dnsfilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dnsfilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.domain_filter = DomainFilter(client)
        self.profile = Profile(client)
