"""FortiOS CMDB - Ca category"""

from .import_ import Import

__all__ = [
    "Ca",
    "Import",
]


class Ca:
    """Ca endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ca endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.import_ = Import(client)
