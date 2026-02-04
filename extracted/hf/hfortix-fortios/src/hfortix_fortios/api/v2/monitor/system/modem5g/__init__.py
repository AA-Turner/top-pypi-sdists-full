"""FortiOS CMDB - Modem5g category"""

from .status import Status

__all__ = [
    "Modem5g",
    "Status",
]


class Modem5g:
    """Modem5g endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Modem5g endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.status = Status(client)
