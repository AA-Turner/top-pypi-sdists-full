"""FortiOS CMDB - Network category"""

from .connect import Connect
from .list import List
from .scan import Scan
from .status import Status

__all__ = [
    "Connect",
    "List",
    "Network",
    "Scan",
    "Status",
]


class Network:
    """Network endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Network endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.connect = Connect(client)
        self.list = List(client)
        self.scan = Scan(client)
        self.status = Status(client)
