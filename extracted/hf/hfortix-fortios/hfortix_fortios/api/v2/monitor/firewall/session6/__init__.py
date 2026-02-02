"""FortiOS CMDB - Session6 category"""

from .close_multiple import CloseMultiple

__all__ = [
    "CloseMultiple",
    "Session6",
]


class Session6:
    """Session6 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Session6 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.close_multiple = CloseMultiple(client)
