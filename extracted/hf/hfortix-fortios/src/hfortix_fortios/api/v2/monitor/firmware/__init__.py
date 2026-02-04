"""FortiOS CMDB - Firmware category"""

from .extension_device import ExtensionDevice

__all__ = [
    "ExtensionDevice",
    "Firmware",
]


class Firmware:
    """Firmware endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Firmware endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.extension_device = ExtensionDevice(client)
