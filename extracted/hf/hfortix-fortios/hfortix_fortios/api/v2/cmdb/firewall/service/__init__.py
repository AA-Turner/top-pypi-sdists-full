"""FortiOS CMDB - Service category"""

from .category import Category
from .custom import Custom
from .group import Group

__all__ = [
    "Category",
    "Custom",
    "Group",
    "Service",
]


class Service:
    """Service endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Service endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.category = Category(client)
        self.custom = Custom(client)
        self.group = Group(client)
