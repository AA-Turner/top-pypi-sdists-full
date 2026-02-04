"""FortiOS CMDB - ProxyPolicy category"""

from ..proxy_policy_base import ProxyPolicy as ProxyPolicyBase
from .clear_counters import ClearCounters

__all__ = [
    "ClearCounters",
    "ProxyPolicy",
]


class ProxyPolicy(ProxyPolicyBase):
    """ProxyPolicy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ProxyPolicy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.clear_counters = ClearCounters(client)
