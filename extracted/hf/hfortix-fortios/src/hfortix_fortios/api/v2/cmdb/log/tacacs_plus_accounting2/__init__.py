"""FortiOS CMDB - TacacsPlusAccounting2 category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "TacacsPlusAccounting2",
]


class TacacsPlusAccounting2:
    """TacacsPlusAccounting2 endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """TacacsPlusAccounting2 endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
