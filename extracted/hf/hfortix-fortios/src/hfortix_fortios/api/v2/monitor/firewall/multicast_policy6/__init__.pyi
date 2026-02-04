"""FortiOS CMDB - MulticastPolicy6 category (stub)"""

from typing import Any
from ..multicast_policy6_base import MulticastPolicy6 as MulticastPolicy6Base
from .clear_counters import ClearCounters
from .reset import Reset

class MulticastPolicy6(MulticastPolicy6Base):
    """MulticastPolicy6 endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters
    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
