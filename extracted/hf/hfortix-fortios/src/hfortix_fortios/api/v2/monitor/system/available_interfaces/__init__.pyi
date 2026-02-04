"""FortiOS CMDB - AvailableInterfaces category (stub)"""

from typing import Any
from ..available_interfaces_base import AvailableInterfaces as AvailableInterfacesBase
from .meta import Meta

class AvailableInterfaces(AvailableInterfacesBase):
    """AvailableInterfaces endpoints wrapper for CMDB API."""

    meta: Meta

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
