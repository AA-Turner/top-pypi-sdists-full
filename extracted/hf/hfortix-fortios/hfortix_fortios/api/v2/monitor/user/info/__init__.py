"""FortiOS CMDB - Info category"""

from .query import Query
from .thumbnail import Thumbnail
from .thumbnail_file import ThumbnailFile

__all__ = [
    "Info",
    "Query",
    "Thumbnail",
    "ThumbnailFile",
]


class Info:
    """Info endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Info endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.query = Query(client)
        self.thumbnail = Thumbnail(client)
        self.thumbnail_file = ThumbnailFile(client)
