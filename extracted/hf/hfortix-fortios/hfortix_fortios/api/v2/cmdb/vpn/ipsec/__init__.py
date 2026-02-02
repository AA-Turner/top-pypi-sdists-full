"""FortiOS CMDB - Ipsec category"""

from .concentrator import Concentrator
from .fec import Fec
from .manualkey import Manualkey
from .manualkey_interface import ManualkeyInterface
from .phase1 import Phase1
from .phase1_interface import Phase1Interface
from .phase2 import Phase2
from .phase2_interface import Phase2Interface

__all__ = [
    "Concentrator",
    "Fec",
    "Ipsec",
    "Manualkey",
    "ManualkeyInterface",
    "Phase1",
    "Phase1Interface",
    "Phase2",
    "Phase2Interface",
]


class Ipsec:
    """Ipsec endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Ipsec endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.concentrator = Concentrator(client)
        self.fec = Fec(client)
        self.manualkey = Manualkey(client)
        self.manualkey_interface = ManualkeyInterface(client)
        self.phase1 = Phase1(client)
        self.phase1_interface = Phase1Interface(client)
        self.phase2 = Phase2(client)
        self.phase2_interface = Phase2Interface(client)
