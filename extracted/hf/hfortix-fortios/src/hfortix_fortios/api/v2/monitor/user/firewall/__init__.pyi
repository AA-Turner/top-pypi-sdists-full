"""FortiOS CMDB - Firewall category (stub)"""

from typing import Any
from ..firewall_base import Firewall as FirewallBase
from .auth import Auth
from .count import Count
from .deauth import Deauth

class Firewall(FirewallBase):
    """Firewall endpoints wrapper for CMDB API."""

    auth: Auth
    count: Count
    deauth: Deauth

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
