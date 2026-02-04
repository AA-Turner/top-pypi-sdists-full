"""FortiOS CMDB - Ntp category"""

from .status import Status

__all__ = [
    "Ntp",
    "Status",
]


class Ntp:
    """Ntp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ntp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
