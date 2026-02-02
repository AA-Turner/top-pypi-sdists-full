"""FortiOS CMDB - Interface category"""

from ..interface_base import Interface as InterfaceBase
from .dhcp_renew import DhcpRenew
from .dhcp_status import DhcpStatus
from .kernel_interfaces import KernelInterfaces
from .poe import Poe
from .poe_usage import PoeUsage
from .speed_test_status import SpeedTestStatus
from .speed_test_trigger import SpeedTestTrigger
from .transceivers import Transceivers
from .wake_on_lan import WakeOnLan

__all__ = [
    "DhcpRenew",
    "DhcpStatus",
    "Interface",
    "KernelInterfaces",
    "Poe",
    "PoeUsage",
    "SpeedTestStatus",
    "SpeedTestTrigger",
    "Transceivers",
    "WakeOnLan",
]


class Interface(InterfaceBase):
    """Interface endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """Interface endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        super().__init__(client)  # Initialize base class with GET methods
        self.dhcp_renew = DhcpRenew(client)
        self.dhcp_status = DhcpStatus(client)
        self.kernel_interfaces = KernelInterfaces(client)
        self.poe = Poe(client)
        self.poe_usage = PoeUsage(client)
        self.speed_test_status = SpeedTestStatus(client)
        self.speed_test_trigger = SpeedTestTrigger(client)
        self.transceivers = Transceivers(client)
        self.wake_on_lan = WakeOnLan(client)
