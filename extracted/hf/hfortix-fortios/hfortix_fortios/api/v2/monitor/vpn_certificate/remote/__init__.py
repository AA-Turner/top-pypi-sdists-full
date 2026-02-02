"""FortiOS CMDB - Remote category"""

from .import_ import Import

__all__ = [
    "Import",
    "Remote",
]


class Remote:
    """Remote endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Remote endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.import_ = Import(client)
