"""FortiOS CMDB - VpnCertificate category"""

from . import ca
from . import crl
from . import csr
from . import local
from . import remote
from .cert_name_available import CertNameAvailable

__all__ = [
    "Ca",
    "CertNameAvailable",
    "Crl",
    "Csr",
    "Local",
    "Remote",
    "VpnCertificate",
]


class VpnCertificate:
    """VpnCertificate endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """VpnCertificate endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.ca = ca.Ca(client)
        self.crl = crl.Crl(client)
        self.csr = csr.Csr(client)
        self.local = local.Local(client)
        self.remote = remote.Remote(client)
        self.cert_name_available = CertNameAvailable(client)
