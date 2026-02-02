"""FortiOS CMDB - LteModem category"""

from .status import Status
from .upgrade import Upgrade
from .upload import Upload

__all__ = [
    "LteModem",
    "Status",
    "Upgrade",
    "Upload",
]


class LteModem:
    """LteModem endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """LteModem endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
        self.upgrade = Upgrade(client)
        self.upload = Upload(client)
