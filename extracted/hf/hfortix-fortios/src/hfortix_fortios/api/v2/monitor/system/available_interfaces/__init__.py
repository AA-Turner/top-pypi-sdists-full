"""FortiOS CMDB - AvailableInterfaces category"""

from ..available_interfaces_base import AvailableInterfaces as AvailableInterfacesBase
from .meta import Meta

__all__ = [
    "AvailableInterfaces",
    "Meta",
]


class AvailableInterfaces(AvailableInterfacesBase):
    """AvailableInterfaces endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """AvailableInterfaces endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.meta = Meta(client)
