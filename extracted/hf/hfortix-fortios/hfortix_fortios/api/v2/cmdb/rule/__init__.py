"""FortiOS CMDB - Rule category"""

from .fmwp import Fmwp
from .iotd import Iotd
from .otdt import Otdt
from .otvp import Otvp

__all__ = [
    "Fmwp",
    "Iotd",
    "Otdt",
    "Otvp",
    "Rule",
]


class Rule:
    """Rule endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Rule endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.fmwp = Fmwp(client)
        self.iotd = Iotd(client)
        self.otdt = Otdt(client)
        self.otvp = Otvp(client)
