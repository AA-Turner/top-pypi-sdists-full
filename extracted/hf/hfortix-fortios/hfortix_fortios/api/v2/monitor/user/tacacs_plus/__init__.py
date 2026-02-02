"""FortiOS CMDB - TacacsPlus category"""

from .test import Test

__all__ = [
    "TacacsPlus",
    "Test",
]


class TacacsPlus:
    """TacacsPlus endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlus endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.test = Test(client)
