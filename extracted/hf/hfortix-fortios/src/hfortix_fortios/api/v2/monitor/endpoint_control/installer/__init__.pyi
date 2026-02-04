"""FortiOS CMDB - Installer category (stub)"""

from typing import Any
from ..installer_base import Installer as InstallerBase
from .download import Download

class Installer(InstallerBase):
    """Installer endpoints wrapper for CMDB API."""

    download: Download

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
