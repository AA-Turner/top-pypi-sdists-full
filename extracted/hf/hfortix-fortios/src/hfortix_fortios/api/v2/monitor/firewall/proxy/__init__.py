"""FortiOS CMDB - Proxy category"""

from .sessions import Sessions

__all__ = [
    "Proxy",
    "Sessions",
]


class Proxy:
    """Proxy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Proxy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.sessions = Sessions(client)
