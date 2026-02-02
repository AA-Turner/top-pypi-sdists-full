"""FortiOS CMDB - Vpn category"""

from . import ike
from . import ipsec
from . import ssl

__all__ = [
    "Ike",
    "Ipsec",
    "Ssl",
    "Vpn",
]


class Vpn:
    """Vpn endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Vpn endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.ike = ike.Ike(client)
        self.ipsec = ipsec.Ipsec(client)
        self.ssl = ssl.Ssl(client)
