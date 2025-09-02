import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Security(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def acl(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/acl", sn=self.sn)

    @computed_field
    @property
    def acl_interface(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/acl/interfaces", sn=self.sn)

    @computed_field
    @property
    def acl_global_policies(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/acl/global-policies", sn=self.sn)

    @computed_field
    @property
    def dmvpn(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/dmvpn", sn=self.sn)

    @computed_field
    @property
    def dhcp_snooping(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/dhcp/snooping", sn=self.sn)

    @computed_field
    @property
    def dhcp_snooping_bindings(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/dhcp/bindings", sn=self.sn)

    @computed_field
    @property
    def ipsec_tunnels(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/ipsec/tunnels", sn=self.sn)

    @computed_field
    @property
    def ipsec_gateways(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/ipsec/gateways", sn=self.sn)

    @computed_field
    @property
    def secure_ports_devices(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/secure-ports/devices", sn=self.sn)

    @computed_field
    @property
    def secure_ports_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/secure-ports/interfaces", sn=self.sn)

    @computed_field
    @property
    def secure_ports_users(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/secure-ports/users", sn=self.sn)

    @computed_field
    @property
    def zone_firewall_policies(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/zone-firewall/policies", sn=self.sn)

    @computed_field
    @property
    def zone_firewall_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/zone-firewall/interfaces", sn=self.sn)

    @computed_field
    @property
    def lsvpn_gateways(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/lsvpn/gateways", sn=self.sn)

    @computed_field
    @property
    def lsvpn_satellites(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/lsvpn/satellites", sn=self.sn)
