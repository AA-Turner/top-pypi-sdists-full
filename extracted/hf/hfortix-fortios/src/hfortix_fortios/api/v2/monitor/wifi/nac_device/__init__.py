"""FortiOS CMDB - NacDevice category"""

from .stats import Stats

__all__ = [
    "NacDevice",
    "Stats",
]


class NacDevice:
    """NacDevice endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """NacDevice endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.stats = Stats(client)
