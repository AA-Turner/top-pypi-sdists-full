"""FortiOS CMDB - HscalefwLicense category"""

from .upload import Upload

__all__ = [
    "HscalefwLicense",
    "Upload",
]


class HscalefwLicense:
    """HscalefwLicense endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """HscalefwLicense endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.upload = Upload(client)
