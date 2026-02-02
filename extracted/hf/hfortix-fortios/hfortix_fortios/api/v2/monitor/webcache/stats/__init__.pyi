"""FortiOS CMDB - Stats category (stub)"""

from typing import Any
from ..stats_base import Stats as StatsBase
from .reset import Reset

class Stats(StatsBase):
    """Stats endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
