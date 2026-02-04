"""FortiOS CMDB - Wanopt category"""

from . import history
from . import peer_stats
from . import webcache

__all__ = [
    "History",
    "PeerStats",
    "Wanopt",
    "Webcache",
]


class Wanopt:
    """Wanopt endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Wanopt endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.history = history.History(client)
        self.peer_stats = peer_stats.PeerStats(client)
        self.webcache = webcache.Webcache(client)
