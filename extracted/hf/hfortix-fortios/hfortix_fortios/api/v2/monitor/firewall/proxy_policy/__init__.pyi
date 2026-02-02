"""FortiOS CMDB - ProxyPolicy category (stub)"""

from typing import Any
from ..proxy_policy_base import ProxyPolicy as ProxyPolicyBase
from .clear_counters import ClearCounters

class ProxyPolicy(ProxyPolicyBase):
    """ProxyPolicy endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
