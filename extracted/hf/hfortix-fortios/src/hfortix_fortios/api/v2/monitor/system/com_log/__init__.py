"""FortiOS CMDB - ComLog category"""

from .download import Download
from .dump import Dump
from .update import Update

__all__ = [
    "ComLog",
    "Download",
    "Dump",
    "Update",
]


class ComLog:
    """ComLog endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ComLog endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
        self.dump = Dump(client)
        self.update = Update(client)
