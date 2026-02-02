"""FortiOS CMDB - PeerStats category (stub)"""

from typing import Any
from ..peer_stats_base import PeerStats as PeerStatsBase
from .reset import Reset

class PeerStats(PeerStatsBase):
    """PeerStats endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
