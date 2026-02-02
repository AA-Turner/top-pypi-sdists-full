"""FortiOS CMDB - Ipmacbinding category"""

from .setting import Setting
from .table import Table

__all__ = [
    "Ipmacbinding",
    "Setting",
    "Table",
]


class Ipmacbinding:
    """Ipmacbinding endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ipmacbinding endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.setting = Setting(client)
        self.table = Table(client)
