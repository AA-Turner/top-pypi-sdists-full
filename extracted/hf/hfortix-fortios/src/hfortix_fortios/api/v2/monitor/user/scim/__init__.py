"""FortiOS CMDB - Scim category"""

from .groups import Groups
from .users import Users

__all__ = [
    "Groups",
    "Scim",
    "Users",
]


class Scim:
    """Scim endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Scim endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.groups = Groups(client)
        self.users = Users(client)
