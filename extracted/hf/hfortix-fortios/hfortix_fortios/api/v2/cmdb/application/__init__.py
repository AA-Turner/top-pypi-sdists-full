"""FortiOS CMDB - Application category"""

from .custom import Custom
from .group import Group
from .list import List
from .name import Name
from .rule_settings import RuleSettings

__all__ = [
    "Application",
    "Custom",
    "Group",
    "List",
    "Name",
    "RuleSettings",
]


class Application:
    """Application endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Application endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.custom = Custom(client)
        self.group = Group(client)
        self.list = List(client)
        self.name = Name(client)
        self.rule_settings = RuleSettings(client)
