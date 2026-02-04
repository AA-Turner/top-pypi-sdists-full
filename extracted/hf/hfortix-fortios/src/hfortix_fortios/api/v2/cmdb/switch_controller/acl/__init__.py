"""FortiOS CMDB - Acl category"""

from .group import Group
from .ingress import Ingress

__all__ = [
    "Acl",
    "Group",
    "Ingress",
]


class Acl:
    """Acl endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Acl endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.group = Group(client)
        self.ingress = Ingress(client)
