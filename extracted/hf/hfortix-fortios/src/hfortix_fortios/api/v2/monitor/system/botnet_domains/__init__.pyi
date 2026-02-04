"""FortiOS CMDB - BotnetDomains category (stub)"""

from typing import Any
from ..botnet_domains_base import BotnetDomains as BotnetDomainsBase
from .hits import Hits
from .stat import Stat

class BotnetDomains(BotnetDomainsBase):
    """BotnetDomains endpoints wrapper for CMDB API."""

    hits: Hits
    stat: Stat

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
