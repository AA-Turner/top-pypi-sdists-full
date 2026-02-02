"""FortiOS CMDB - ChangePassword category"""

from .select import Select

__all__ = [
    "ChangePassword",
    "Select",
]


class ChangePassword:
    """ChangePassword endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ChangePassword endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.select = Select(client)
