import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Stp(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def bridges(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/bridges", sn=self.sn)

    @computed_field
    @property
    def instances(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/instances", sn=self.sn)

    @computed_field
    @property
    def instance_members(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/instance-members", sn=self.sn)

    @computed_field
    @property
    def vlans(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/vlans", sn=self.sn)

    @computed_field
    @property
    def ports(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/ports", sn=self.sn)

    @computed_field
    @property
    def neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/neighbors", sn=self.sn)

    @computed_field
    @property
    def guards(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/guards", sn=self.sn)

    @computed_field
    @property
    def inconsistencies(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/inconsistencies/summary", sn=self.sn)

    @computed_field
    @property
    def inconsistencies_details(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/inconsistencies/details", sn=self.sn)

    @computed_field
    @property
    def inconsistencies_ports_vlan_mismatch(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/spanning-tree/inconsistencies/neighbor-ports-vlan-mismatch", sn=self.sn
        )

    @computed_field
    @property
    def inconsistencies_ports_multiple_neighbors(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/spanning-tree/inconsistencies/ports-multiple-neighbors", sn=self.sn
        )

    @computed_field
    @property
    def inconsistencies_stp_cdp_ports_mismatch(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/spanning-tree/inconsistencies/stp-cdp-ports-mismatch", sn=self.sn
        )

    @computed_field
    @property
    def inconsistencies_multiple_stp(self) -> Table:
        return Table(client=self.client, endpoint="tables/spanning-tree/inconsistencies/multiple-stp", sn=self.sn)
