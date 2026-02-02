"""FortiOS CMDB - Extender category (stub)"""

from typing import Any
from ..extender_base import Extender as ExtenderBase
from .diagnose import Diagnose
from .modem_firmware import ModemFirmware
from .reset import Reset
from .upgrade import Upgrade

class Extender(ExtenderBase):
    """Extender endpoints wrapper for CMDB API."""

    diagnose: Diagnose
    modem_firmware: ModemFirmware
    reset: Reset
    upgrade: Upgrade

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
