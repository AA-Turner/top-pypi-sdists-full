"""FortiOS CMDB - SctpFilter category"""

from .profile import Profile

__all__ = [
    "Profile",
    "SctpFilter",
]


class SctpFilter:
    """SctpFilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SctpFilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.profile = Profile(client)
