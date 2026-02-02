"""FortiOS CMDB - ApProfile category"""

from .create_default import CreateDefault

__all__ = [
    "ApProfile",
    "CreateDefault",
]


class ApProfile:
    """ApProfile endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ApProfile endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.create_default = CreateDefault(client)
