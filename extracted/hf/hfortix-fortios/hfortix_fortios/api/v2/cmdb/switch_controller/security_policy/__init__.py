"""FortiOS CMDB - SecurityPolicy category"""

from .local_access import LocalAccess
from .x802_1x import X8021x

__all__ = [
    "LocalAccess",
    "SecurityPolicy",
    "X8021x",
]


class SecurityPolicy:
    """SecurityPolicy endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """SecurityPolicy endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.local_access = LocalAccess(client)
        self.x802_1x = X8021x(client)
