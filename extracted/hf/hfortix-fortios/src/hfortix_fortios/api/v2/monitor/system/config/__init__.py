"""FortiOS CMDB - Config category"""

from .backup import Backup
from .restore import Restore
from .restore_status import RestoreStatus
from .usb_filelist import UsbFilelist

__all__ = [
    "Backup",
    "Config",
    "Restore",
    "RestoreStatus",
    "UsbFilelist",
]


class Config:
    """Config endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Config endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.backup = Backup(client)
        self.restore = Restore(client)
        self.restore_status = RestoreStatus(client)
        self.usb_filelist = UsbFilelist(client)
