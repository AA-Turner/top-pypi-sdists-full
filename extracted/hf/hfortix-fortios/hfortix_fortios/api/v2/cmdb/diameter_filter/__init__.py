"""FortiOS CMDB - DiameterFilter category"""

from .profile import Profile

__all__ = [
    "DiameterFilter",
    "Profile",
]


class DiameterFilter:
    """DiameterFilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """DiameterFilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.profile = Profile(client)
