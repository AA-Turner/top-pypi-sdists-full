"""FortiOS CMDB - BlacklistedCertificates category"""

from ..blacklisted_certificates_base import BlacklistedCertificates as BlacklistedCertificatesBase
from .statistics import Statistics

__all__ = [
    "BlacklistedCertificates",
    "Statistics",
]


class BlacklistedCertificates(BlacklistedCertificatesBase):
    """BlacklistedCertificates endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """BlacklistedCertificates endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.statistics = Statistics(client)
