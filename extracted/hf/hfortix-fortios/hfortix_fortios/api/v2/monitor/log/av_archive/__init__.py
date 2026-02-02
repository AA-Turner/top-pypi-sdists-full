"""FortiOS CMDB - AvArchive category"""

from .download import Download

__all__ = [
    "AvArchive",
    "Download",
]


class AvArchive:
    """AvArchive endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """AvArchive endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
