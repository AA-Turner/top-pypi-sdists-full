"""FortiOS CMDB - Disk category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Disk",
    "Filter",
    "Setting",
]


class Disk:
    """Disk endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Disk endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
