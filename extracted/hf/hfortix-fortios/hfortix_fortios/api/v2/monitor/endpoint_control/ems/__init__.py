"""FortiOS CMDB - Ems category"""

from .cert_status import CertStatus
from .malware_hash import MalwareHash
from .status import Status
from .status_summary import StatusSummary
from .unverify_cert import UnverifyCert
from .verify_cert import VerifyCert

__all__ = [
    "CertStatus",
    "Ems",
    "MalwareHash",
    "Status",
    "StatusSummary",
    "UnverifyCert",
    "VerifyCert",
]


class Ems:
    """Ems endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ems endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.cert_status = CertStatus(client)
        self.malware_hash = MalwareHash(client)
        self.status = Status(client)
        self.status_summary = StatusSummary(client)
        self.unverify_cert = UnverifyCert(client)
        self.verify_cert = VerifyCert(client)
