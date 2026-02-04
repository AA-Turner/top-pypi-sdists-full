"""FortiOS CMDB - ConfigErrorLog category"""

from .download import Download

__all__ = [
    "ConfigErrorLog",
    "Download",
]


class ConfigErrorLog:
    """ConfigErrorLog endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ConfigErrorLog endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
