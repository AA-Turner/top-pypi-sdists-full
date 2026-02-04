"""FortiOS CMDB - Proxy category"""

from ..proxy_base import Proxy as ProxyBase
from .count import Count

__all__ = [
    "Count",
    "Proxy",
]


class Proxy(ProxyBase):
    """Proxy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Proxy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.count = Count(client)
