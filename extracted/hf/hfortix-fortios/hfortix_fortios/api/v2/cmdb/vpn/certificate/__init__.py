"""FortiOS CMDB - Certificate category"""

from .ca import Ca
from .crl import Crl
from .hsm_local import HsmLocal
from .local import Local
from .ocsp_server import OcspServer
from .remote import Remote
from .setting import Setting

__all__ = [
    "Ca",
    "Certificate",
    "Crl",
    "HsmLocal",
    "Local",
    "OcspServer",
    "Remote",
    "Setting",
]


class Certificate:
    """Certificate endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Certificate endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.ca = Ca(client)
        self.crl = Crl(client)
        self.hsm_local = HsmLocal(client)
        self.local = Local(client)
        self.ocsp_server = OcspServer(client)
        self.remote = Remote(client)
        self.setting = Setting(client)
