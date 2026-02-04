"""FortiOS CMDB - Banned category"""

from ..banned_base import Banned as BannedBase
from .add_users import AddUsers
from .check import Check
from .clear_all import ClearAll
from .clear_users import ClearUsers

__all__ = [
    "AddUsers",
    "Banned",
    "Check",
    "ClearAll",
    "ClearUsers",
]


class Banned(BannedBase):
    """Banned endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Banned endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.add_users = AddUsers(client)
        self.check = Check(client)
        self.clear_all = ClearAll(client)
        self.clear_users = ClearUsers(client)
