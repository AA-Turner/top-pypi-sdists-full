"""FortiOS CMDB - Admin category"""

from .change_vdom_mode import ChangeVdomMode

__all__ = [
    "Admin",
    "ChangeVdomMode",
]


class Admin:
    """Admin endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Admin endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.change_vdom_mode = ChangeVdomMode(client)
