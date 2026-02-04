"""FortiOS CMDB - UpgradeReport category"""

from .current import Current
from .exists import Exists
from .saved import Saved

__all__ = [
    "Current",
    "Exists",
    "Saved",
    "UpgradeReport",
]


class UpgradeReport:
    """UpgradeReport endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """UpgradeReport endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.current = Current(client)
        self.exists = Exists(client)
        self.saved = Saved(client)
