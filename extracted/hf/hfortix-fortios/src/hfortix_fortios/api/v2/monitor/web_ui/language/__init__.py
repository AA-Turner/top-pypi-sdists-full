"""FortiOS CMDB - Language category"""

from .import_ import Import

__all__ = [
    "Import",
    "Language",
]


class Language:
    """Language endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Language endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.import_ = Import(client)
