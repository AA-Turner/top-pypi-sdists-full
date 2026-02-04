"""FortiOS CMDB - BlacklistedCertificates category (stub)"""

from typing import Any
from ..blacklisted_certificates_base import BlacklistedCertificates as BlacklistedCertificatesBase
from .statistics import Statistics

class BlacklistedCertificates(BlacklistedCertificatesBase):
    """BlacklistedCertificates endpoints wrapper for CMDB API."""

    statistics: Statistics

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
