"""FortiOS CMDB - Os category"""

from .reboot import Reboot
from .shutdown import Shutdown

__all__ = [
    "Os",
    "Reboot",
    "Shutdown",
]


class Os:
    """Os endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Os endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.reboot = Reboot(client)
        self.shutdown = Shutdown(client)
