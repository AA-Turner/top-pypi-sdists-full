"""FortiOS CMDB - Pacfile category"""

from .download import Download
from .upload import Upload

__all__ = [
    "Download",
    "Pacfile",
    "Upload",
]


class Pacfile:
    """Pacfile endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Pacfile endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
        self.upload = Upload(client)
