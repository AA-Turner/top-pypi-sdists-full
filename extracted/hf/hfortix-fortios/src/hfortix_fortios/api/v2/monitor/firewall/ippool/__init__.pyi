"""FortiOS CMDB - Ippool category (stub)"""

from typing import Any
from ..ippool_base import Ippool as IppoolBase
from .mapping import Mapping

class Ippool(IppoolBase):
    """Ippool endpoints wrapper for CMDB API."""

    mapping: Mapping

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
