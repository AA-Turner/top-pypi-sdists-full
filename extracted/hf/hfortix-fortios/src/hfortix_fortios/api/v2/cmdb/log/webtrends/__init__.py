"""FortiOS CMDB - Webtrends category"""

from .filter import Filter
from .setting import Setting

__all__ = [
    "Filter",
    "Setting",
    "Webtrends",
]


class Webtrends:
    """Webtrends endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Webtrends endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.setting = Setting(client)
