"""FortiOS CMDB - UsbLog category"""

from ..usb_log_base import UsbLog as UsbLogBase
from .start import Start
from .stop import Stop

__all__ = [
    "Start",
    "Stop",
    "UsbLog",
]


class UsbLog(UsbLogBase):
    """UsbLog endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """UsbLog endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.start = Start(client)
        self.stop = Stop(client)
