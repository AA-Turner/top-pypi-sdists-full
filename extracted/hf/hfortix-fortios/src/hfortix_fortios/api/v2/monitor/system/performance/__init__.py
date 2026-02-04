"""FortiOS CMDB - Performance category"""

from .status import Status

__all__ = [
    "Performance",
    "Status",
]


class Performance:
    """Performance endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Performance endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
