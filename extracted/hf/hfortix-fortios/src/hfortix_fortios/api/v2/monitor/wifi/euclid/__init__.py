"""FortiOS CMDB - Euclid category"""

from ..euclid_base import Euclid as EuclidBase
from .reset import Reset

__all__ = [
    "Euclid",
    "Reset",
]


class Euclid(EuclidBase):
    """Euclid endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Euclid endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
