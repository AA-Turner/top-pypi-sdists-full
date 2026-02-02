"""FortiOS CMDB - PerIpShaper category"""

from ..per_ip_shaper_base import PerIpShaper as PerIpShaperBase
from .reset import Reset

__all__ = [
    "PerIpShaper",
    "Reset",
]


class PerIpShaper(PerIpShaperBase):
    """PerIpShaper endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """PerIpShaper endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.reset = Reset(client)
