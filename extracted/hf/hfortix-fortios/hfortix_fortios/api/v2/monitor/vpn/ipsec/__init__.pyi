"""FortiOS CMDB - Ipsec category (stub)"""

from typing import Any
from ..ipsec_base import Ipsec as IpsecBase
from .connection_count import ConnectionCount
from .tunnel_down import TunnelDown
from .tunnel_reset_stats import TunnelResetStats
from .tunnel_up import TunnelUp

class Ipsec(IpsecBase):
    """Ipsec endpoints wrapper for CMDB API."""

    connection_count: ConnectionCount
    tunnel_down: TunnelDown
    tunnel_reset_stats: TunnelResetStats
    tunnel_up: TunnelUp

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
