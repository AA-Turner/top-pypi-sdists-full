import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Sdn(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def aci_endpoints(self) -> Table:
        return Table(client=self.client, endpoint="tables/aci/endpoints", sn=self.sn)

    @computed_field
    @property
    def aci_vlan(self) -> Table:
        return Table(client=self.client, endpoint="tables/aci/vlan", sn=self.sn)

    @computed_field
    @property
    def aci_vrf(self) -> Table:
        return Table(client=self.client, endpoint="tables/aci/vrf", sn=self.sn)

    @computed_field
    @property
    def aci_dtep(self) -> Table:
        return Table(client=self.client, endpoint="tables/aci/dtep", sn=self.sn)

    @computed_field
    @property
    def vxlan_vtep(self) -> Table:
        return Table(client=self.client, endpoint="tables/vxlan/vtep", sn=self.sn)

    @computed_field
    @property
    def vxlan_peers(self) -> Table:
        return Table(client=self.client, endpoint="tables/vxlan/peers", sn=self.sn)

    @computed_field
    @property
    def vxlan_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/vxlan/interfaces", sn=self.sn)

    @computed_field
    @property
    def vxlan_vni(self) -> Table:
        return Table(client=self.client, endpoint="tables/vxlan/vni", sn=self.sn)

    @computed_field
    @property
    def apic_controllers(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/controllers", sn=self.sn)

    @computed_field
    @property
    def apic_contexts(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/contexts", sn=self.sn)

    @computed_field
    @property
    def apic_bridge_domains(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/bridge-domains", sn=self.sn)

    @computed_field
    @property
    def apic_applications(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/applications", sn=self.sn)

    @computed_field
    @property
    def apic_endpoint_groups(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/endpoint-groups", sn=self.sn)

    @computed_field
    @property
    def apic_endpoint_groups_contracts(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/endpoint-groups/contracts", sn=self.sn)

    @computed_field
    @property
    def apic_contracts(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/contracts", sn=self.sn)

    @computed_field
    @property
    def apic_service_graphs(self) -> Table:
        return Table(client=self.client, endpoint="tables/apic/service-graphs", sn=self.sn)
