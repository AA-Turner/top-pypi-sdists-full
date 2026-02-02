"""FortiOS CMDB - Session category"""

from .cancel import Cancel

__all__ = [
    "Cancel",
    "Session",
]


class Session:
    """Session endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Session endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.cancel = Cancel(client)
