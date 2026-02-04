"""FortiOS CMDB - Session category"""

from .performance import Performance

__all__ = [
    "Performance",
    "Session",
]


class Session:
    """Session endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Session endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.performance = Performance(client)
