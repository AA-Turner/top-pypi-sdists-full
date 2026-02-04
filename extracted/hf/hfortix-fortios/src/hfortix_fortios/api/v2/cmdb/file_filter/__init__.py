"""FortiOS CMDB - FileFilter category"""

from .profile import Profile

__all__ = [
    "FileFilter",
    "Profile",
]


class FileFilter:
    """FileFilter endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """FileFilter endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.profile = Profile(client)
