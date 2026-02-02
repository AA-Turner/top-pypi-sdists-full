"""FortiOS CMDB - Automation category"""

from .setting import Setting

__all__ = [
    "Automation",
    "Setting",
]


class Automation:
    """Automation endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Automation endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.setting = Setting(client)
