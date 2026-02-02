"""FortiOS CMDB - MaliciousUrls category (stub)"""

from typing import Any
from ..malicious_urls_base import MaliciousUrls as MaliciousUrlsBase
from .stat import Stat

class MaliciousUrls(MaliciousUrlsBase):
    """MaliciousUrls endpoints wrapper for CMDB API."""

    stat: Stat

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
