"""FortiOS CMDB - Crl category"""

from .import_ import Import

__all__ = [
    "Crl",
    "Import",
]


class Crl:
    """Crl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Crl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.import_ = Import(client)
