"""FortiOS CMDB - ConfigSync category"""

from .status import Status

__all__ = [
    "ConfigSync",
    "Status",
]


class ConfigSync:
    """ConfigSync endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ConfigSync endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
