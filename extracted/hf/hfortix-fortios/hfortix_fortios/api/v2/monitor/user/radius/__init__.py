"""FortiOS CMDB - Radius category"""

from .get_test_connect import GetTestConnect
from .test_connect import TestConnect

__all__ = [
    "GetTestConnect",
    "Radius",
    "TestConnect",
]


class Radius:
    """Radius endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Radius endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.get_test_connect = GetTestConnect(client)
        self.test_connect = TestConnect(client)
