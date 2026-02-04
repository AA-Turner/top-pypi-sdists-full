"""FortiOS CMDB - Icap category"""

from .profile import Profile
from .server import Server
from .server_group import ServerGroup

__all__ = [
    "Icap",
    "Profile",
    "Server",
    "ServerGroup",
]


class Icap:
    """Icap endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Icap endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.profile = Profile(client)
        self.server = Server(client)
        self.server_group = ServerGroup(client)
