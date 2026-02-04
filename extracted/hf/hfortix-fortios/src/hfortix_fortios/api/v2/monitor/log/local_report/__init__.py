"""FortiOS CMDB - LocalReport category"""

from .delete import Delete
from .download import Download

__all__ = [
    "Delete",
    "Download",
    "LocalReport",
]


class LocalReport:
    """LocalReport endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """LocalReport endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.delete = Delete(client)
        self.download = Download(client)
