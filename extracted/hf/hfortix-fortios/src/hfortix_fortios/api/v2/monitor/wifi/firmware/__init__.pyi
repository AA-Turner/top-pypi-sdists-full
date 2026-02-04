"""FortiOS CMDB - Firmware category (stub)"""

from typing import Any
from ..firmware_base import Firmware as FirmwareBase
from .download import Download
from .push import Push
from .upload import Upload

class Firmware(FirmwareBase):
    """Firmware endpoints wrapper for CMDB API."""

    download: Download
    push: Push
    upload: Upload

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
