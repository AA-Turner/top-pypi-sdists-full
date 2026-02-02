"""FortiOS CMDB - Stats category"""

from ..stats_base import Stats as StatsBase
from .reset import Reset

__all__ = [
    "Reset",
    "Stats",
]


class Stats(StatsBase):
    """Stats endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Stats endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
