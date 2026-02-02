"""FortiOS CMDB - Fortiview category"""

from . import session
from .historical_statistics import HistoricalStatistics
from .realtime_proxy_statistics import RealtimeProxyStatistics
from .realtime_statistics import RealtimeStatistics

__all__ = [
    "Fortiview",
    "HistoricalStatistics",
    "RealtimeProxyStatistics",
    "RealtimeStatistics",
    "Session",
]


class Fortiview:
    """Fortiview endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortiview endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.session = session.Session(client)
        self.historical_statistics = HistoricalStatistics(client)
        self.realtime_proxy_statistics = RealtimeProxyStatistics(client)
        self.realtime_statistics = RealtimeStatistics(client)
