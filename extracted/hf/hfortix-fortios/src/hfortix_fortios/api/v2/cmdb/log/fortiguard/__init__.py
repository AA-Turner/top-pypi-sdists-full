"""FortiOS CMDB - Fortiguard category"""

from .filter import Filter
from .override_filter import OverrideFilter
from .override_setting import OverrideSetting
from .setting import Setting

__all__ = [
    "Filter",
    "Fortiguard",
    "OverrideFilter",
    "OverrideSetting",
    "Setting",
]


class Fortiguard:
    """Fortiguard endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortiguard endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.override_filter = OverrideFilter(client)
        self.override_setting = OverrideSetting(client)
        self.setting = Setting(client)
