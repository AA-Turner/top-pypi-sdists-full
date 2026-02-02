"""FortiOS CMDB - Override category"""

from ..override_base import Override as OverrideBase
from .delete import Delete

__all__ = [
    "Delete",
    "Override",
]


class Override(OverrideBase):
    """Override endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Override endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.delete = Delete(client)
