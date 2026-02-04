"""FortiOS CMDB - Fortimanager category"""

from .backup_action import BackupAction
from .backup_details import BackupDetails
from .backup_summary import BackupSummary

__all__ = [
    "BackupAction",
    "BackupDetails",
    "BackupSummary",
    "Fortimanager",
]


class Fortimanager:
    """Fortimanager endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Fortimanager endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.backup_action = BackupAction(client)
        self.backup_details = BackupDetails(client)
        self.backup_summary = BackupSummary(client)
