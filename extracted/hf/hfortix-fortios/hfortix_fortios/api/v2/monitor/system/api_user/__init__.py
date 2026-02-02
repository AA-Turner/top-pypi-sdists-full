"""FortiOS CMDB - ApiUser category"""

from .generate_key import GenerateKey

__all__ = [
    "ApiUser",
    "GenerateKey",
]


class ApiUser:
    """ApiUser endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ApiUser endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.generate_key = GenerateKey(client)
