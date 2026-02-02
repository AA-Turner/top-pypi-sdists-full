"""FortiOS CMDB - ForticloudReport category"""

from .download import Download

__all__ = [
    "Download",
    "ForticloudReport",
]


class ForticloudReport:
    """ForticloudReport endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ForticloudReport endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
