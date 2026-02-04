"""FortiOS CMDB - WildcardFqdn category"""

from .custom import Custom
from .group import Group

__all__ = [
    "Custom",
    "Group",
    "WildcardFqdn",
]


class WildcardFqdn:
    """WildcardFqdn endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """WildcardFqdn endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.custom = Custom(client)
        self.group = Group(client)
