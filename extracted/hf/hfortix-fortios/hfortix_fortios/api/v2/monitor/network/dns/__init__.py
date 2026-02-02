"""FortiOS CMDB - Dns category"""

from .latency import Latency

__all__ = [
    "Dns",
    "Latency",
]


class Dns:
    """Dns endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Dns endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.latency = Latency(client)
