"""FortiOS CMDB - Client category"""

from ..client_base import Client as ClientBase
from .disassociate import Disassociate

__all__ = [
    "Client",
    "Disassociate",
]


class Client(ClientBase):
    """Client endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Client endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.disassociate = Disassociate(client)
