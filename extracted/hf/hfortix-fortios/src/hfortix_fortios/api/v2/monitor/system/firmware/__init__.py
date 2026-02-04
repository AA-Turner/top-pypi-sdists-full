"""FortiOS CMDB - Firmware category"""

from ..firmware_base import Firmware as FirmwareBase
from .upgrade import Upgrade
from .upgrade_paths import UpgradePaths

__all__ = [
    "Firmware",
    "Upgrade",
    "UpgradePaths",
]


class Firmware(FirmwareBase):
    """Firmware endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Firmware endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.upgrade = Upgrade(client)
        self.upgrade_paths = UpgradePaths(client)
