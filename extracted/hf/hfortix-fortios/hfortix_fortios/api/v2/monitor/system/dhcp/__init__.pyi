"""FortiOS CMDB - Dhcp category (stub)"""

from typing import Any
from ..dhcp_base import Dhcp as DhcpBase
from .revoke import Revoke

class Dhcp(DhcpBase):
    """Dhcp endpoints wrapper for CMDB API."""

    revoke: Revoke

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
