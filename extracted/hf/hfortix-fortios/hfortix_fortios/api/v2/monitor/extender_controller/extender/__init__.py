"""FortiOS CMDB - Extender category"""

from ..extender_base import Extender as ExtenderBase
from .diagnose import Diagnose
from .modem_firmware import ModemFirmware
from .reset import Reset
from .upgrade import Upgrade

__all__ = [
    "Diagnose",
    "Extender",
    "ModemFirmware",
    "Reset",
    "Upgrade",
]


class Extender(ExtenderBase):
    """Extender endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Extender endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.diagnose = Diagnose(client)
        self.modem_firmware = ModemFirmware(client)
        self.reset = Reset(client)
        self.upgrade = Upgrade(client)
