"""FortiOS CMDB - Certificate category"""

from .download import Download
from .read_info import ReadInfo

__all__ = [
    "Certificate",
    "Download",
    "ReadInfo",
]


class Certificate:
    """Certificate endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Certificate endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
        self.read_info = ReadInfo(client)
