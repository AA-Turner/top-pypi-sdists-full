"""FortiOS CMDB - RegionImage category (stub)"""

from typing import Any
from ..region_image_base import RegionImage as RegionImageBase
from .upload import Upload

class RegionImage(RegionImageBase):
    """RegionImage endpoints wrapper for CMDB API."""

    upload: Upload

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
