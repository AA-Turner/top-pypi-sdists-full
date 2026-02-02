"""FortiOS CMDB - Vpn category"""

from . import certificate
from . import ipsec
from .kmip_server import KmipServer
from .l2tp import L2tp
from .pptp import Pptp
from .qkd import Qkd

__all__ = [
    "Certificate",
    "Ipsec",
    "KmipServer",
    "L2tp",
    "Pptp",
    "Qkd",
    "Vpn",
]


class Vpn:
    """Vpn endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Vpn endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.certificate = certificate.Certificate(client)
        self.ipsec = ipsec.Ipsec(client)
        self.kmip_server = KmipServer(client)
        self.l2tp = L2tp(client)
        self.pptp = Pptp(client)
        self.qkd = Qkd(client)
