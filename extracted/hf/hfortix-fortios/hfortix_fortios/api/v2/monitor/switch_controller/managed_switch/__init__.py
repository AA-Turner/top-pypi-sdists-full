"""FortiOS CMDB - ManagedSwitch category"""

from .bios import Bios
from .bounce_port import BouncePort
from .cable_status import CableStatus
from .dhcp_snooping import DhcpSnooping
from .faceplate_xml import FaceplateXml
from .factory_reset import FactoryReset
from .health_status import HealthStatus
from .models import Models
from .poe_reset import PoeReset
from .port_health import PortHealth
from .port_stats import PortStats
from .port_stats_reset import PortStatsReset
from .restart import Restart
from .status import Status
from .transceivers import Transceivers
from .tx_rx import TxRx
from .update import Update

__all__ = [
    "Bios",
    "BouncePort",
    "CableStatus",
    "DhcpSnooping",
    "FaceplateXml",
    "FactoryReset",
    "HealthStatus",
    "ManagedSwitch",
    "Models",
    "PoeReset",
    "PortHealth",
    "PortStats",
    "PortStatsReset",
    "Restart",
    "Status",
    "Transceivers",
    "TxRx",
    "Update",
]


class ManagedSwitch:
    """ManagedSwitch endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """ManagedSwitch endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.bios = Bios(client)
        self.bounce_port = BouncePort(client)
        self.cable_status = CableStatus(client)
        self.dhcp_snooping = DhcpSnooping(client)
        self.faceplate_xml = FaceplateXml(client)
        self.factory_reset = FactoryReset(client)
        self.health_status = HealthStatus(client)
        self.models = Models(client)
        self.poe_reset = PoeReset(client)
        self.port_health = PortHealth(client)
        self.port_stats = PortStats(client)
        self.port_stats_reset = PortStatsReset(client)
        self.restart = Restart(client)
        self.status = Status(client)
        self.transceivers = Transceivers(client)
        self.tx_rx = TxRx(client)
        self.update = Update(client)
