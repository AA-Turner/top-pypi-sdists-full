"""FortiOS CMDB - Ippool category"""

from ..ippool_base import Ippool as IppoolBase
from .mapping import Mapping

__all__ = [
    "Ippool",
    "Mapping",
]


class Ippool(IppoolBase):
    """Ippool endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ippool endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.mapping = Mapping(client)
