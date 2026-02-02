"""FortiOS CMDB - FtpProxy category"""

from .explicit import Explicit

__all__ = [
    "Explicit",
    "FtpProxy",
]


class FtpProxy:
    """FtpProxy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """FtpProxy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.explicit = Explicit(client)
