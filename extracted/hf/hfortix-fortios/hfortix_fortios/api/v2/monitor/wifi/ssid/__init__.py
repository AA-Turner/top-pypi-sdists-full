"""FortiOS CMDB - Ssid category"""

from .generate_keys import GenerateKeys

__all__ = [
    "GenerateKeys",
    "Ssid",
]


class Ssid:
    """Ssid endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ssid endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.generate_keys = GenerateKeys(client)
