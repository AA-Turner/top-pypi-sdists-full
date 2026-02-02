"""FortiOS CMDB - FswFirmware category (stub)"""

from typing import Any
from ..fsw_firmware_base import FswFirmware as FswFirmwareBase
from .download import Download
from .push import Push
from .upload import Upload

class FswFirmware(FswFirmwareBase):
    """FswFirmware endpoints wrapper for CMDB API."""

    download: Download
    push: Push
    upload: Upload

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
