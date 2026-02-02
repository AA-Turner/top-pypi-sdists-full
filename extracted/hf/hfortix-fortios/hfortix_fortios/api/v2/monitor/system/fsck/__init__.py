"""FortiOS CMDB - Fsck category"""

from .start import Start

__all__ = [
    "Fsck",
    "Start",
]


class Fsck:
    """Fsck endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fsck endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.start = Start(client)
