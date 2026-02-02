"""FortiOS CMDB - Ptp category"""

from .interface_policy import InterfacePolicy
from .profile import Profile

__all__ = [
    "InterfacePolicy",
    "Profile",
    "Ptp",
]


class Ptp:
    """Ptp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ptp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.interface_policy = InterfacePolicy(client)
        self.profile = Profile(client)
