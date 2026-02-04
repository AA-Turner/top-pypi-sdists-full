"""FortiOS CMDB - DebugFlow category"""

from .start import Start
from .stop import Stop

__all__ = [
    "DebugFlow",
    "Start",
    "Stop",
]


class DebugFlow:
    """DebugFlow endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """DebugFlow endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.start = Start(client)
        self.stop = Stop(client)
