"""FortiOS CMDB - Report category"""

from .layout import Layout
from .setting import Setting

__all__ = [
    "Layout",
    "Report",
    "Setting",
]


class Report:
    """Report endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Report endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.layout = Layout(client)
        self.setting = Setting(client)
