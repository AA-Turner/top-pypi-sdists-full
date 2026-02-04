"""FortiOS CMDB - ZtnaFirewallPolicy category"""

from .clear_counters import ClearCounters

__all__ = [
    "ClearCounters",
    "ZtnaFirewallPolicy",
]


class ZtnaFirewallPolicy:
    """ZtnaFirewallPolicy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ZtnaFirewallPolicy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.clear_counters = ClearCounters(client)
