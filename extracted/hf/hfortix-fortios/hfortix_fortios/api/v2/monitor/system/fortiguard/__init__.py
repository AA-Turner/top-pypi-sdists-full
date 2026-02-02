"""FortiOS CMDB - Fortiguard category"""

from .clear_statistics import ClearStatistics
from .manual_update import ManualUpdate
from .server_info import ServerInfo
from .test_availability import TestAvailability
from .update import Update

__all__ = [
    "ClearStatistics",
    "Fortiguard",
    "ManualUpdate",
    "ServerInfo",
    "TestAvailability",
    "Update",
]


class Fortiguard:
    """Fortiguard endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortiguard endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.clear_statistics = ClearStatistics(client)
        self.manual_update = ManualUpdate(client)
        self.server_info = ServerInfo(client)
        self.test_availability = TestAvailability(client)
        self.update = Update(client)
