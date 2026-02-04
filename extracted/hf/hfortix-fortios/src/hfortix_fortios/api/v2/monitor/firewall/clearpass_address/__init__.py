"""FortiOS CMDB - ClearpassAddress category"""

from .add import Add
from .delete import Delete

__all__ = [
    "Add",
    "ClearpassAddress",
    "Delete",
]


class ClearpassAddress:
    """ClearpassAddress endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ClearpassAddress endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.add = Add(client)
        self.delete = Delete(client)
