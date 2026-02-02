"""FortiOS CMDB - Gtp category (stub)"""

from typing import Any
from ..gtp_base import Gtp as GtpBase
from .flush import Flush

class Gtp(GtpBase):
    """Gtp endpoints wrapper for CMDB API."""

    flush: Flush

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
