"""FortiOS CMDB - Ssl category"""

from .setting import Setting

__all__ = [
    "Setting",
    "Ssl",
]


class Ssl:
    """Ssl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ssl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.setting = Setting(client)
