"""FortiOS CMDB - TrafficHistory category"""

from .enable_app_bandwidth_tracking import EnableAppBandwidthTracking
from .interface import Interface
from .top_applications import TopApplications

__all__ = [
    "EnableAppBandwidthTracking",
    "Interface",
    "TopApplications",
    "TrafficHistory",
]


class TrafficHistory:
    """TrafficHistory endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TrafficHistory endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.enable_app_bandwidth_tracking = EnableAppBandwidthTracking(client)
        self.interface = Interface(client)
        self.top_applications = TopApplications(client)
