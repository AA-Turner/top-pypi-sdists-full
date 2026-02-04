"""FortiOS CMDB - Installer category"""

from ..installer_base import Installer as InstallerBase
from .download import Download

__all__ = [
    "Download",
    "Installer",
]


class Installer(InstallerBase):
    """Installer endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Installer endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.download = Download(client)
