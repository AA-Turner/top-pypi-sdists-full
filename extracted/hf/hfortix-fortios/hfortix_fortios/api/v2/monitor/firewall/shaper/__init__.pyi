"""FortiOS CMDB - Shaper category (stub)"""

from typing import Any
from ..shaper_base import Shaper as ShaperBase
from .multi_class_shaper import MultiClassShaper
from .reset import Reset

class Shaper(ShaperBase):
    """Shaper endpoints wrapper for CMDB API."""

    multi_class_shaper: MultiClassShaper
    reset: Reset

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
