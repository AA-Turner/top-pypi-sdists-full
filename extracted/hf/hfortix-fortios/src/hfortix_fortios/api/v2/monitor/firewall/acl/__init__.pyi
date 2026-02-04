"""FortiOS CMDB - Acl category (stub)"""

from typing import Any
from ..acl_base import Acl as AclBase
from .clear_counters import ClearCounters

class Acl(AclBase):
    """Acl endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
