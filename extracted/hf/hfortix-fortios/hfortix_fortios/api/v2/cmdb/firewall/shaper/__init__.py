"""FortiOS CMDB - Shaper category"""

from .per_ip_shaper import PerIpShaper
from .traffic_shaper import TrafficShaper

__all__ = [
    "PerIpShaper",
    "Shaper",
    "TrafficShaper",
]


class Shaper:
    """Shaper endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Shaper endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.per_ip_shaper = PerIpShaper(client)
        self.traffic_shaper = TrafficShaper(client)
