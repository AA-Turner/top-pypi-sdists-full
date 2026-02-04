"""FortiOS CMDB - Ike category"""

from .clear import Clear

__all__ = [
    "Clear",
    "Ike",
]


class Ike:
    """Ike endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ike endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.clear = Clear(client)
