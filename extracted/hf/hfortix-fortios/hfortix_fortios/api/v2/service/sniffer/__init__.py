"""FortiOS CMDB - Sniffer category"""

from .delete import Delete
from .download import Download
from .list import List
from .meta import Meta
from .start import Start
from .stop import Stop

__all__ = [
    "Delete",
    "Download",
    "List",
    "Meta",
    "Sniffer",
    "Start",
    "Stop",
]


class Sniffer:
    """Sniffer endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Sniffer endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.delete = Delete(client)
        self.download = Download(client)
        self.list = List(client)
        self.meta = Meta(client)
        self.start = Start(client)
        self.stop = Stop(client)
