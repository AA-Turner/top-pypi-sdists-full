"""FortiOS CMDB - Acl6 category (stub)"""

from typing import Any
from ..acl6_base import Acl6 as Acl6Base
from .clear_counters import ClearCounters

class Acl6(Acl6Base):
    """Acl6 endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
