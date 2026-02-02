"""FortiOS CMDB - Modem category (stub)"""

from typing import Any
from ..modem_base import Modem as ModemBase
from .connect import Connect
from .disconnect import Disconnect
from .reset import Reset
from .update import Update

class Modem(ModemBase):
    """Modem endpoints wrapper for CMDB API."""

    connect: Connect
    disconnect: Disconnect
    reset: Reset
    update: Update

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
