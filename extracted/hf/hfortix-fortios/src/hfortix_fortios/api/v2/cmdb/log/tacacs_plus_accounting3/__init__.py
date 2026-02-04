"""FortiOS CMDB - TacacsPlusAccounting3 category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusAccounting3",
]


class TacacsPlusAccounting3:
    """TacacsPlusAccounting3 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlusAccounting3 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
