"""FortiOS CMDB - Voip category"""

from .profile import Profile

__all__ = [
    "Profile",
    "Voip",
]


class Voip:
    """Voip endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Voip endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.profile = Profile(client)
