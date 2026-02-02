"""FortiOS CMDB - DisconnectAdmins category"""

from .select import Select

__all__ = [
    "DisconnectAdmins",
    "Select",
]


class DisconnectAdmins:
    """DisconnectAdmins endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """DisconnectAdmins endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.select = Select(client)
