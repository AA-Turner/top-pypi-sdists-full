"""FortiOS CMDB - TacacsPlusAccounting category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusAccounting",
]


class TacacsPlusAccounting:
    """TacacsPlusAccounting endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlusAccounting endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
