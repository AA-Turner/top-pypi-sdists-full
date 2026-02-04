"""FortiOS CMDB - VirtualWan category"""

from .health_check import HealthCheck
from .interface_log import InterfaceLog
from .members import Members
from .sla_log import SlaLog
from .sladb import Sladb

__all__ = [
    "HealthCheck",
    "InterfaceLog",
    "Members",
    "SlaLog",
    "Sladb",
    "VirtualWan",
]


class VirtualWan:
    """VirtualWan endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """VirtualWan endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.health_check = HealthCheck(client)
        self.interface_log = InterfaceLog(client)
        self.members = Members(client)
        self.sla_log = SlaLog(client)
        self.sladb = Sladb(client)
