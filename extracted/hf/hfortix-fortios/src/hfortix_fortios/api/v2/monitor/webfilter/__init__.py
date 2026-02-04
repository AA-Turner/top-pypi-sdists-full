"""FortiOS CMDB - Webfilter category"""

from . import category_quota
from . import malicious_urls
from . import override
from .fortiguard_categories import FortiguardCategories
from .trusted_urls import TrustedUrls

__all__ = [
    "CategoryQuota",
    "FortiguardCategories",
    "MaliciousUrls",
    "Override",
    "TrustedUrls",
    "Webfilter",
]


class Webfilter:
    """Webfilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Webfilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.category_quota = category_quota.CategoryQuota(client)
        self.malicious_urls = malicious_urls.MaliciousUrls(client)
        self.override = override.Override(client)
        self.fortiguard_categories = FortiguardCategories(client)
        self.trusted_urls = TrustedUrls(client)
