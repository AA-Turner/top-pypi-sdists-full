"""FortiOS CMDB - Ssl category (stub)"""

from typing import Any
from ..ssl_base import Ssl as SslBase
from .clear_tunnel import ClearTunnel
from .delete import Delete
from .stats import Stats

class Ssl(SslBase):
    """Ssl endpoints wrapper for CMDB API."""

    clear_tunnel: ClearTunnel
    delete: Delete
    stats: Stats

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
