"""FortiOS CMDB - HaPeer category (stub)"""

from typing import Any
from ..ha_peer_base import HaPeer as HaPeerBase
from .disconnect import Disconnect
from .update import Update

class HaPeer(HaPeerBase):
    """HaPeer endpoints wrapper for CMDB API."""

    disconnect: Disconnect
    update: Update

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
