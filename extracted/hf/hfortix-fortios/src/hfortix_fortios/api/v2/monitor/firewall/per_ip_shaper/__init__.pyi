"""FortiOS CMDB - PerIpShaper category (stub)"""

from typing import Any
from ..per_ip_shaper_base import PerIpShaper as PerIpShaperBase
from .reset import Reset

class PerIpShaper(PerIpShaperBase):
    """PerIpShaper endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
