"""FortiOS CMDB - SecurityRating category"""

from .controls import Controls
from .settings import Settings

__all__ = [
    "Controls",
    "SecurityRating",
    "Settings",
]


class SecurityRating:
    """SecurityRating endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SecurityRating endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.controls = Controls(client)
        self.settings = Settings(client)
