"""FortiOS CMDB - UsbLog category (stub)"""

from typing import Any
from ..usb_log_base import UsbLog as UsbLogBase
from .start import Start
from .stop import Stop

class UsbLog(UsbLogBase):
    """UsbLog endpoints wrapper for CMDB API."""

    start: Start
    stop: Stop

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
