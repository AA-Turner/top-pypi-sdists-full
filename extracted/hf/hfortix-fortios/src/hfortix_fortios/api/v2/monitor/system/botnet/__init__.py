"""FortiOS CMDB - Botnet category"""

from ..botnet_base import Botnet as BotnetBase
from .stat import Stat

__all__ = [
    "Botnet",
    "Stat",
]


class Botnet(BotnetBase):
    """Botnet endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Botnet endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.stat = Stat(client)
