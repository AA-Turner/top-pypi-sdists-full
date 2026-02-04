"""FortiOS CMDB - FortitokenCloud category"""

from .status import Status
from .trial import Trial

__all__ = [
    "FortitokenCloud",
    "Status",
    "Trial",
]


class FortitokenCloud:
    """FortitokenCloud endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """FortitokenCloud endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
        self.trial = Trial(client)
