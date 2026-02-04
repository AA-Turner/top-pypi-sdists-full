"""FortiOS CMDB - Lldp category"""

from .network_policy import NetworkPolicy

__all__ = [
    "Lldp",
    "NetworkPolicy",
]


class Lldp:
    """Lldp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Lldp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.network_policy = NetworkPolicy(client)
