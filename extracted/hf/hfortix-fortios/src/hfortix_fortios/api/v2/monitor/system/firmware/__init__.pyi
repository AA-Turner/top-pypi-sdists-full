"""FortiOS CMDB - Firmware category (stub)"""

from typing import Any
from ..firmware_base import Firmware as FirmwareBase
from .upgrade import Upgrade
from .upgrade_paths import UpgradePaths

class Firmware(FirmwareBase):
    """Firmware endpoints wrapper for CMDB API."""

    upgrade: Upgrade
    upgrade_paths: UpgradePaths

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
