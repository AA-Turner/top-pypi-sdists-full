"""FortiOS CMDB - VirtualPatch category"""

from .profile import Profile

__all__ = [
    "Profile",
    "VirtualPatch",
]


class VirtualPatch:
    """VirtualPatch endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """VirtualPatch endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.profile = Profile(client)
