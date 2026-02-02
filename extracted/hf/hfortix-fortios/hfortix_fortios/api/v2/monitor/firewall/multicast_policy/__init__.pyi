"""FortiOS CMDB - MulticastPolicy category (stub)"""

from typing import Any
from ..multicast_policy_base import MulticastPolicy as MulticastPolicyBase
from .clear_counters import ClearCounters
from .reset import Reset

class MulticastPolicy(MulticastPolicyBase):
    """MulticastPolicy endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters
    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
