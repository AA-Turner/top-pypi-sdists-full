"""FortiOS CMDB - Ipsec category"""

from ..ipsec_base import Ipsec as IpsecBase
from .connection_count import ConnectionCount
from .tunnel_down import TunnelDown
from .tunnel_reset_stats import TunnelResetStats
from .tunnel_up import TunnelUp

__all__ = [
    "ConnectionCount",
    "Ipsec",
    "TunnelDown",
    "TunnelResetStats",
    "TunnelUp",
]


class Ipsec(IpsecBase):
    """Ipsec endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ipsec endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.connection_count = ConnectionCount(client)
        self.tunnel_down = TunnelDown(client)
        self.tunnel_reset_stats = TunnelResetStats(client)
        self.tunnel_up = TunnelUp(client)
