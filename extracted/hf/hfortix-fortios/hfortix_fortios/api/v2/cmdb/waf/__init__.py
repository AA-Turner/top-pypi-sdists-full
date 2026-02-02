"""FortiOS CMDB - Waf category"""

from .main_class import MainClass
from .profile import Profile
from .signature import Signature

__all__ = [
    "MainClass",
    "Profile",
    "Signature",
    "Waf",
]


class Waf:
    """Waf endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Waf endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.main_class = MainClass(client)
        self.profile = Profile(client)
        self.signature = Signature(client)
