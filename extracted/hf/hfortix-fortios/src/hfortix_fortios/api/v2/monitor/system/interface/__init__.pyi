"""FortiOS CMDB - Interface category (stub)"""

from typing import Any
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

class Interface(InterfaceBase):
    """Interface endpoints wrapper for CMDB API."""

    dhcp_renew: DhcpRenew
    dhcp_status: DhcpStatus
    kernel_interfaces: KernelInterfaces
    poe: Poe
    poe_usage: PoeUsage
    speed_test_status: SpeedTestStatus
    speed_test_trigger: SpeedTestTrigger
    transceivers: Transceivers
    wake_on_lan: WakeOnLan

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
