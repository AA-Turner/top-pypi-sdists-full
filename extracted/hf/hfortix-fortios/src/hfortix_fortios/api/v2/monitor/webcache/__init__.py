"""FortiOS CMDB - Webcache category"""

from . import stats

__all__ = [
    "Stats",
    "Webcache",
]


class Webcache:
    """Webcache endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Webcache endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.stats = stats.Stats(client)
