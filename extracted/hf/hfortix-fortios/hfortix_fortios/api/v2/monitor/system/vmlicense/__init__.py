"""FortiOS CMDB - Vmlicense category"""

from .download import Download
from .download_eval import DownloadEval
from .upload import Upload

__all__ = [
    "Download",
    "DownloadEval",
    "Upload",
    "Vmlicense",
]


class Vmlicense:
    """Vmlicense endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Vmlicense endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.download = Download(client)
        self.download_eval = DownloadEval(client)
        self.upload = Upload(client)
