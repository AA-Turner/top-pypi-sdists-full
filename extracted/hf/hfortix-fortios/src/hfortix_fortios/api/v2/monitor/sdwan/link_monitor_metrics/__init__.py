"""FortiOS CMDB - LinkMonitorMetrics category"""

from .report import Report

__all__ = [
    "LinkMonitorMetrics",
    "Report",
]


class LinkMonitorMetrics:
    """LinkMonitorMetrics endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """LinkMonitorMetrics endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.report = Report(client)
