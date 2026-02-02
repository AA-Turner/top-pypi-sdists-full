"""FortiOS CMDB - Object category"""

from .usage import Usage

__all__ = [
    "Object",
    "Usage",
]


class Object:
    """Object endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Object endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.usage = Usage(client)
