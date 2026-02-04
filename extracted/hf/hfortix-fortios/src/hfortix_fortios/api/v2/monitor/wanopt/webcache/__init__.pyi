"""FortiOS CMDB - Webcache category (stub)"""

from typing import Any
from ..webcache_base import Webcache as WebcacheBase
from .reset import Reset

class Webcache(WebcacheBase):
    """Webcache endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
