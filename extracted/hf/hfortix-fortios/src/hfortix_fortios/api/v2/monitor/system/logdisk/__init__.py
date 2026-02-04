"""FortiOS CMDB - Logdisk category"""

from .format import Format

__all__ = [
    "Format",
    "Logdisk",
]


class Logdisk:
    """Logdisk endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Logdisk endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.format = Format(client)
