"""FortiOS CMDB - Local category"""

from .change_password import ChangePassword

__all__ = [
    "ChangePassword",
    "Local",
]


class Local:
    """Local endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Local endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.change_password = ChangePassword(client)
