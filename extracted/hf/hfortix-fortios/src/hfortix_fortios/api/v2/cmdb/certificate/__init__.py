"""FortiOS CMDB - Certificate category"""

from .ca import Ca
from .crl import Crl
from .hsm_local import HsmLocal
from .local import Local
from .remote import Remote

__all__ = [
    "Ca",
    "Certificate",
    "Crl",
    "HsmLocal",
    "Local",
    "Remote",
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
        self.remote = Remote(client)
