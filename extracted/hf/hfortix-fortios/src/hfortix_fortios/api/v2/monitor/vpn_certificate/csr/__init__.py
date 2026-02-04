"""FortiOS CMDB - Csr category"""

from .generate import Generate

__all__ = [
    "Csr",
    "Generate",
]


class Csr:
    """Csr endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Csr endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.generate = Generate(client)
