"""FortiOS CMDB - Lookup category (stub)"""

from typing import Any
from ..lookup_base import Lookup as LookupBase
from .ha_peer import HaPeer

class Lookup(LookupBase):
    """Lookup endpoints wrapper for CMDB API."""

    ha_peer: HaPeer

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
