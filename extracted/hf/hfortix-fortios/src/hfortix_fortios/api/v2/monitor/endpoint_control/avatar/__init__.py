"""FortiOS CMDB - Avatar category"""

from .download import Download

__all__ = [
    "Avatar",
    "Download",
]


class Avatar:
    """Avatar endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Avatar endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
