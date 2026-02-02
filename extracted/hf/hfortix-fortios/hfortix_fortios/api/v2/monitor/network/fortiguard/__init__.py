"""FortiOS CMDB - Fortiguard category"""

from .live_services_latency import LiveServicesLatency

__all__ = [
    "Fortiguard",
    "LiveServicesLatency",
]


class Fortiguard:
    """Fortiguard endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortiguard endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.live_services_latency = LiveServicesLatency(client)
