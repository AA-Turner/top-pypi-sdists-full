"""FortiOS CMDB - UsbDevice category"""

from .eject import Eject

__all__ = [
    "Eject",
    "UsbDevice",
]


class UsbDevice:
    """UsbDevice endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """UsbDevice endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.eject = Eject(client)
