"""FortiOS CMDB - Sdwan category"""

from . import link_monitor_metrics

__all__ = [
    "LinkMonitorMetrics",
    "Sdwan",
]


class Sdwan:
    """Sdwan endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Sdwan endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.link_monitor_metrics = link_monitor_metrics.LinkMonitorMetrics(client)
