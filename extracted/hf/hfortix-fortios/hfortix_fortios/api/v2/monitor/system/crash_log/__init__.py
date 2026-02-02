"""FortiOS CMDB - CrashLog category"""

from .clear import Clear
from .download import Download

__all__ = [
    "Clear",
    "CrashLog",
    "Download",
]


class CrashLog:
    """CrashLog endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """CrashLog endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.clear = Clear(client)
        self.download = Download(client)
