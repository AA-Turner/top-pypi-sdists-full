"""FortiOS CMDB - Time category"""

from ..time_base import Time as TimeBase
from .set import Set

__all__ = [
    "Set",
    "Time",
]


class Time(TimeBase):
    """Time endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Time endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.set = Set(client)
