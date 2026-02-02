"""FortiOS CMDB - CentralManagement category"""

from .status import Status

__all__ = [
    "CentralManagement",
    "Status",
]


class CentralManagement:
    """CentralManagement endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """CentralManagement endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
