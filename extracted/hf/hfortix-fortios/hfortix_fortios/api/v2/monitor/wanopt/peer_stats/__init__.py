"""FortiOS CMDB - PeerStats category"""

from ..peer_stats_base import PeerStats as PeerStatsBase
from .reset import Reset

__all__ = [
    "PeerStats",
    "Reset",
]


class PeerStats(PeerStatsBase):
    """PeerStats endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """PeerStats endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
