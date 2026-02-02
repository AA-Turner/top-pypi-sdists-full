"""FortiOS CMDB - Alertemail category"""

from .setting import Setting

__all__ = [
    "Alertemail",
    "Setting",
]


class Alertemail:
    """Alertemail endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Alertemail endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.setting = Setting(client)
