"""FortiOS CMDB - Snmp category"""

from .community import Community
from .mib_view import MibView
from .rmon_stat import RmonStat
from .sysinfo import Sysinfo
from .user import User

__all__ = [
    "Community",
    "MibView",
    "RmonStat",
    "Snmp",
    "Sysinfo",
    "User",
]


class Snmp:
    """Snmp endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Snmp endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.community = Community(client)
        self.mib_view = MibView(client)
        self.rmon_stat = RmonStat(client)
        self.sysinfo = Sysinfo(client)
        self.user = User(client)
