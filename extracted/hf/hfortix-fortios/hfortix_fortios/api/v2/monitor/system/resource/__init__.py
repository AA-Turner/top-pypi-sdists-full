"""FortiOS CMDB - Resource category"""

from .usage import Usage

__all__ = [
    "Resource",
    "Usage",
]


class Resource:
    """Resource endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Resource endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.usage = Usage(client)
