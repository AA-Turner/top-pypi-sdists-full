"""FortiOS CMDB - Schedule category"""

from .group import Group
from .onetime import Onetime
from .recurring import Recurring

__all__ = [
    "Group",
    "Onetime",
    "Recurring",
    "Schedule",
]


class Schedule:
    """Schedule endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Schedule endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.group = Group(client)
        self.onetime = Onetime(client)
        self.recurring = Recurring(client)
