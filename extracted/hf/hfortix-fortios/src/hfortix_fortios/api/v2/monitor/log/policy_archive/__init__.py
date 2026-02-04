"""FortiOS CMDB - PolicyArchive category"""

from .download import Download

__all__ = [
    "Download",
    "PolicyArchive",
]


class PolicyArchive:
    """PolicyArchive endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """PolicyArchive endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
