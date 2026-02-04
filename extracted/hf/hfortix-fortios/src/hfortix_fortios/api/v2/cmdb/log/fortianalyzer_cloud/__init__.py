"""FortiOS CMDB - FortianalyzerCloud category"""

from .filter import Filter
from .override_filter import OverrideFilter
from .override_setting import OverrideSetting
from .setting import Setting

__all__ = [
    "Filter",
    "FortianalyzerCloud",
    "OverrideFilter",
    "OverrideSetting",
    "Setting",
]


class FortianalyzerCloud:
    """FortianalyzerCloud endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """FortianalyzerCloud endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.filter = Filter(client)
        self.override_filter = OverrideFilter(client)
        self.override_setting = OverrideSetting(client)
        self.setting = Setting(client)
