"""FortiOS CMDB - Debug category"""

from .download import Download

__all__ = [
    "Debug",
    "Download",
]


class Debug:
    """Debug endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Debug endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
