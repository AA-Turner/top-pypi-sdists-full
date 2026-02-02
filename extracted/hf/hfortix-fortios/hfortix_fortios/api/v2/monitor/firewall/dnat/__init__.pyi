"""FortiOS CMDB - Dnat category (stub)"""

from typing import Any
from ..dnat_base import Dnat as DnatBase
from .clear_counters import ClearCounters
from .reset import Reset

class Dnat(DnatBase):
    """Dnat endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters
    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
