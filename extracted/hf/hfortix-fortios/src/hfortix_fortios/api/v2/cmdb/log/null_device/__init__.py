"""FortiOS CMDB - NullDevice category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "NullDevice",
    "Setting",
]


class NullDevice:
    """NullDevice endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """NullDevice endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
