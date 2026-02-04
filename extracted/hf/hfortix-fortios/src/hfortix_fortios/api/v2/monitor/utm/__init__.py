"""FortiOS CMDB - Utm category"""

from . import antivirus
from . import blacklisted_certificates
from . import rating_lookup
from .app_lookup import AppLookup
from .application_categories import ApplicationCategories

__all__ = [
    "Antivirus",
    "AppLookup",
    "ApplicationCategories",
    "BlacklistedCertificates",
    "RatingLookup",
    "Utm",
]


class Utm:
    """Utm endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Utm endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.antivirus = antivirus.Antivirus(client)
        self.blacklisted_certificates = blacklisted_certificates.BlacklistedCertificates(client)
        self.rating_lookup = rating_lookup.RatingLookup(client)
        self.app_lookup = AppLookup(client)
        self.application_categories = ApplicationCategories(client)
