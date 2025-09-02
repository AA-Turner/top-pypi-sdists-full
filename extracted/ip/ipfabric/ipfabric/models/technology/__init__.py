from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table
from .addressing import Addressing
from .cloud import Cloud
from .dhcp import Dhcp
from .fhrp import Fhrp
from .interfaces import Interfaces
from .ip_telephony import IpTelephony
from .load_balancing import LoadBalancing
from .managed_networks import ManagedNetworks
from .management import Management
from .mpls import Mpls
from .multicast import Multicast
from .neighbors import Neighbors
from .oam import Oam
from .platforms import Platforms
from .port_channels import PortChannels
from .qos import Qos
from .routing import Routing
from .sdn import Sdn
from .sdwan import Sdwan
from .security import Security
from .stp import Stp
from .vlans import Vlans
from .wireless import Wireless


class Technology(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    def print_menus(self):
        print(
            sorted(
                [
                    _
                    for _ in dir(self)
                    if _[0] != "_" and not isinstance(getattr(self, _), Table) and hasattr(getattr(self, _), "client")
                ]
            )
        )

    @computed_field
    @property
    def platforms(self) -> Platforms:
        return Platforms(client=self.client, sn=self.sn)

    @computed_field
    @property
    def interfaces(self) -> Interfaces:
        return Interfaces(client=self.client, sn=self.sn)

    @computed_field
    @property
    def neighbors(self) -> Neighbors:
        return Neighbors(client=self.client, sn=self.sn)

    @computed_field
    @property
    def dhcp(self) -> Dhcp:
        return Dhcp(client=self.client, sn=self.sn)

    @computed_field
    @property
    def port_channels(self) -> PortChannels:
        return PortChannels(client=self.client, sn=self.sn)

    @computed_field
    @property
    def vlans(self) -> Vlans:
        return Vlans(client=self.client, sn=self.sn)

    @computed_field
    @property
    def stp(self) -> Stp:
        return Stp(client=self.client, sn=self.sn)

    @computed_field
    @property
    def addressing(self) -> Addressing:
        return Addressing(client=self.client, sn=self.sn)

    @computed_field
    @property
    def fhrp(self) -> Fhrp:
        return Fhrp(client=self.client, sn=self.sn)

    @computed_field
    @property
    def managed_networks(self) -> ManagedNetworks:
        return ManagedNetworks(client=self.client, sn=self.sn)

    @computed_field
    @property
    def mpls(self) -> Mpls:
        return Mpls(client=self.client, sn=self.sn)

    @computed_field
    @property
    def multicast(self) -> Multicast:
        return Multicast(client=self.client, sn=self.sn)

    @computed_field
    @property
    def cloud(self) -> Cloud:
        return Cloud(client=self.client, sn=self.sn)

    @computed_field
    @property
    def management(self) -> Management:
        return Management(client=self.client, sn=self.sn)

    @computed_field
    @property
    def ip_telephony(self) -> IpTelephony:
        return IpTelephony(client=self.client, sn=self.sn)

    @computed_field
    @property
    def load_balancing(self) -> LoadBalancing:
        return LoadBalancing(client=self.client, sn=self.sn)

    @computed_field
    @property
    def oam(self) -> Oam:
        return Oam(client=self.client, sn=self.sn)

    @computed_field
    @property
    def qos(self) -> Qos:
        return Qos(client=self.client, sn=self.sn)

    @computed_field
    @property
    def routing(self) -> Routing:
        return Routing(client=self.client, sn=self.sn)

    @computed_field
    @property
    def sdn(self) -> Sdn:
        return Sdn(client=self.client, sn=self.sn)

    @computed_field
    @property
    def sdwan(self) -> Sdwan:
        return Sdwan(client=self.client, sn=self.sn)

    @computed_field
    @property
    def security(self) -> Security:
        return Security(client=self.client, sn=self.sn)

    @computed_field
    @property
    def wireless(self) -> Wireless:
        return Wireless(client=self.client, sn=self.sn)

    @computed_field
    @property
    def serial_ports(self) -> Table:
        return Table(client=self.client, endpoint="tables/serial-ports", sn=self.sn)


__all__ = ["Technology"]
