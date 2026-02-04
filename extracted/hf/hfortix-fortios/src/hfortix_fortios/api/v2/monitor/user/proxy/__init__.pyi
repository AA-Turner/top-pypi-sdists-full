"""FortiOS CMDB - Proxy category (stub)"""

from typing import Any
from ..proxy_base import Proxy as ProxyBase
from .count import Count

class Proxy(ProxyBase):
    """Proxy endpoints wrapper for CMDB API."""

    count: Count

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
