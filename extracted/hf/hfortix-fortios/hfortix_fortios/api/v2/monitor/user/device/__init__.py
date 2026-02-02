"""FortiOS CMDB - Device category"""

from .iot_query import IotQuery
from .purdue_level import PurdueLevel
from .query import Query
from .stats import Stats

__all__ = [
    "Device",
    "IotQuery",
    "PurdueLevel",
    "Query",
    "Stats",
]


class Device:
    """Device endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Device endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.iot_query = IotQuery(client)
        self.purdue_level = PurdueLevel(client)
        self.query = Query(client)
        self.stats = Stats(client)
