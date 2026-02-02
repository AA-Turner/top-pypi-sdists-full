"""FortiOS CMDB - Firmware category"""

from ..firmware_base import Firmware as FirmwareBase
from .download import Download
from .push import Push
from .upload import Upload

__all__ = [
    "Download",
    "Firmware",
    "Push",
    "Upload",
]


class Firmware(FirmwareBase):
    """Firmware endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Firmware endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.download = Download(client)
        self.push = Push(client)
        self.upload = Upload(client)
