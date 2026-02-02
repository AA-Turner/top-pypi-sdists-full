"""FortiOS CMDB - Local category"""

from .create import Create
from .import_ import Import

__all__ = [
    "Create",
    "Import",
    "Local",
]


class Local:
    """Local endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Local endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.create = Create(client)
        self.import_ = Import(client)
