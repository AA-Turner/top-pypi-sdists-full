"""FortiOS CMDB - Sandbox category"""

from .cloud_regions import CloudRegions
from .connection import Connection
from .detect import Detect
from .stats import Stats
from .status import Status

__all__ = [
    "CloudRegions",
    "Connection",
    "Detect",
    "Sandbox",
    "Stats",
    "Status",
]


class Sandbox:
    """Sandbox endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Sandbox endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.cloud_regions = CloudRegions(client)
        self.connection = Connection(client)
        self.detect = Detect(client)
        self.stats = Stats(client)
        self.status = Status(client)
