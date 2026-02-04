"""FortiOS CMDB - RegionImage category"""

from ..region_image_base import RegionImage as RegionImageBase
from .upload import Upload

__all__ = [
    "RegionImage",
    "Upload",
]


class RegionImage(RegionImageBase):
    """RegionImage endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """RegionImage endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.upload = Upload(client)
