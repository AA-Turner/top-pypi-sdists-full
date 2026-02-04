"""FortiOS CMDB - Memory category"""

from .filter import Filter
from .global_setting import GlobalSetting
from .setting import Setting

__all__ = [
    "Filter",
    "GlobalSetting",
    "Memory",
    "Setting",
]


class Memory:
    """Memory endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Memory endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.global_setting = GlobalSetting(client)
        self.setting = Setting(client)
