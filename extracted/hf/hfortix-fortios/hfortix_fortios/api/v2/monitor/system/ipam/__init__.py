"""FortiOS CMDB - Ipam category"""

from .list import List
from .status import Status
from .utilization import Utilization

__all__ = [
    "Ipam",
    "List",
    "Status",
    "Utilization",
]


class Ipam:
    """Ipam endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ipam endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.list = List(client)
        self.status = Status(client)
        self.utilization = Utilization(client)
