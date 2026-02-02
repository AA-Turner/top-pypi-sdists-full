"""FortiOS CMDB - Euclid category (stub)"""

from typing import Any
from ..euclid_base import Euclid as EuclidBase
from .reset import Reset

class Euclid(EuclidBase):
    """Euclid endpoints wrapper for CMDB API."""

    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
