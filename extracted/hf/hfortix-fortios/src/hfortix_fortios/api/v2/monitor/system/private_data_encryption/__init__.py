"""FortiOS CMDB - PrivateDataEncryption category"""

from .set import Set

__all__ = [
    "PrivateDataEncryption",
    "Set",
]


class PrivateDataEncryption:
    """PrivateDataEncryption endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """PrivateDataEncryption endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.set = Set(client)
