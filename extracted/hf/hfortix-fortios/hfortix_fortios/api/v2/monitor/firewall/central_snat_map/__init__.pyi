"""FortiOS CMDB - CentralSnatMap category (stub)"""

from typing import Any
from ..central_snat_map_base import CentralSnatMap as CentralSnatMapBase
from .clear_counters import ClearCounters
from .reset import Reset

class CentralSnatMap(CentralSnatMapBase):
    """CentralSnatMap endpoints wrapper for CMDB API."""

    clear_counters: ClearCounters
    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
