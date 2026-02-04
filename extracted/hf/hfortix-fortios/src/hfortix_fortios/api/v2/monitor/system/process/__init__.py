"""FortiOS CMDB - Process category"""

from .kill import Kill

__all__ = [
    "Kill",
    "Process",
]


class Process:
    """Process endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Process endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.kill = Kill(client)
