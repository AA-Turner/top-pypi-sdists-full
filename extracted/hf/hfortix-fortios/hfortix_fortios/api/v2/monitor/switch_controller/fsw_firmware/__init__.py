"""FortiOS CMDB - FswFirmware category"""

from ..fsw_firmware_base import FswFirmware as FswFirmwareBase
from .download import Download
from .push import Push
from .upload import Upload

__all__ = [
    "Download",
    "FswFirmware",
    "Push",
    "Upload",
]


class FswFirmware(FswFirmwareBase):
    """FswFirmware endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """FswFirmware endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.download = Download(client)
        self.push = Push(client)
        self.upload = Upload(client)
