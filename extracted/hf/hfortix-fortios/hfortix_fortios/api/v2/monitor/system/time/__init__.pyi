"""FortiOS CMDB - Time category (stub)"""

from typing import Any
from ..time_base import Time as TimeBase
from .set import Set

class Time(TimeBase):
    """Time endpoints wrapper for CMDB API."""

    set: Set

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
