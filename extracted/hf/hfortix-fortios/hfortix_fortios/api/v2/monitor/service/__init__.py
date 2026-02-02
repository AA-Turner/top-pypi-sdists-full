"""FortiOS CMDB - Service category"""

from . import ldap

__all__ = [
    "Ldap",
    "Service",
]


class Service:
    """Service endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Service endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.ldap = ldap.Ldap(client)
