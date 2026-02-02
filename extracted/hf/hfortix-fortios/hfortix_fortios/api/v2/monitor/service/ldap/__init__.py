"""FortiOS CMDB - Ldap category"""

from .query import Query

__all__ = [
    "Ldap",
    "Query",
]


class Ldap:
    """Ldap endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ldap endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.query = Query(client)
