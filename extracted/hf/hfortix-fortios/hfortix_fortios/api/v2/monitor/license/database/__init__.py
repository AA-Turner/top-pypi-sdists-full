"""FortiOS CMDB - Database category"""

from .upgrade import Upgrade

__all__ = [
    "Database",
    "Upgrade",
]


class Database:
    """Database endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Database endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.upgrade = Upgrade(client)
