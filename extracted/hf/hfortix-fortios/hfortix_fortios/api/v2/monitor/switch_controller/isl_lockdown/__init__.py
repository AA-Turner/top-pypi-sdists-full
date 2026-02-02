"""FortiOS CMDB - IslLockdown category"""

from .status import Status
from .update import Update

__all__ = [
    "IslLockdown",
    "Status",
    "Update",
]


class IslLockdown:
    """IslLockdown endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """IslLockdown endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
        self.update = Update(client)
