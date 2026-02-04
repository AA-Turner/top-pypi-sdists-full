"""FortiOS CMDB - License category"""

from . import database
from .fortianalyzer_status import FortianalyzerStatus
from .forticare_org_list import ForticareOrgList
from .forticare_resellers import ForticareResellers
from .status import Status

__all__ = [
    "Database",
    "FortianalyzerStatus",
    "ForticareOrgList",
    "ForticareResellers",
    "License",
    "Status",
]


class License:
    """License endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """License endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.database = database.Database(client)
        self.fortianalyzer_status = FortianalyzerStatus(client)
        self.forticare_org_list = ForticareOrgList(client)
        self.forticare_resellers = ForticareResellers(client)
        self.status = Status(client)
