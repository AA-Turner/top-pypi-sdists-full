"""FortiOS CMDB - Shaper category"""

from ..shaper_base import Shaper as ShaperBase
from .multi_class_shaper import MultiClassShaper
from .reset import Reset

__all__ = [
    "MultiClassShaper",
    "Reset",
    "Shaper",
]


class Shaper(ShaperBase):
    """Shaper endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Shaper endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.multi_class_shaper = MultiClassShaper(client)
        self.reset = Reset(client)
