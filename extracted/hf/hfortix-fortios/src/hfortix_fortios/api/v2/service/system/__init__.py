"""FortiOS CMDB - System category"""

from .fabric_admin_lockout_exists_on_firmware_update import FabricAdminLockoutExistsOnFirmwareUpdate
from .fabric_time_in_sync import FabricTimeInSync
from .psirt_vulnerabilities import PsirtVulnerabilities

__all__ = [
    "FabricAdminLockoutExistsOnFirmwareUpdate",
    "FabricTimeInSync",
    "PsirtVulnerabilities",
    "System",
]


class System:
    """System endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """System endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.fabric_admin_lockout_exists_on_firmware_update = FabricAdminLockoutExistsOnFirmwareUpdate(client)
        self.fabric_time_in_sync = FabricTimeInSync(client)
        self.psirt_vulnerabilities = PsirtVulnerabilities(client)
