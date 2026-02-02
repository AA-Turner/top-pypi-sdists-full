"""FortiOS CMDB - Modem3g category"""

from .custom import Custom

__all__ = [
    "Custom",
    "Modem3g",
]


class Modem3g:
    """Modem3g endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Modem3g endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.custom = Custom(client)
