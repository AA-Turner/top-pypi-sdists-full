"""FortiOS CMDB - Antivirus category"""

from .stats import Stats

__all__ = [
    "Antivirus",
    "Stats",
]


class Antivirus:
    """Antivirus endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Antivirus endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.stats = Stats(client)
