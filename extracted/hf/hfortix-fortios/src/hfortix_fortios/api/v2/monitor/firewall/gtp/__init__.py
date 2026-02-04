"""FortiOS CMDB - Gtp category"""

from ..gtp_base import Gtp as GtpBase
from .flush import Flush

__all__ = [
    "Flush",
    "Gtp",
]


class Gtp(GtpBase):
    """Gtp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Gtp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.flush = Flush(client)
