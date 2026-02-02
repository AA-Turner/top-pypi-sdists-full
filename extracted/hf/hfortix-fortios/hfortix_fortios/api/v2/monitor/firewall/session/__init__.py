"""FortiOS CMDB - Session category"""

from .close import Close
from .close_all import CloseAll
from .close_multiple import CloseMultiple

__all__ = [
    "Close",
    "CloseAll",
    "CloseMultiple",
    "Session",
]


class Session:
    """Session endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Session endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.close = Close(client)
        self.close_all = CloseAll(client)
        self.close_multiple = CloseMultiple(client)
