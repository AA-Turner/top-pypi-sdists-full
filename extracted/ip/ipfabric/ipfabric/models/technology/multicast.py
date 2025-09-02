import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Multicast(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def pim_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/pim/neighbors", sn=self.sn)

    @computed_field
    @property
    def pim_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/pim/interfaces", sn=self.sn)

    @computed_field
    @property
    def mroute_overview(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/routes/overview", sn=self.sn)

    @computed_field
    @property
    def mroute_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/routes/table", sn=self.sn)

    @computed_field
    @property
    def mroute_oil_detail(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/routes/outgoing-interfaces", sn=self.sn)

    @computed_field
    @property
    def mroute_counters(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/routes/counters", sn=self.sn)

    @computed_field
    @property
    def mroute_first_hop_router(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/routes/first-hop-router", sn=self.sn)

    @computed_field
    @property
    def mroute_sources(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/routes/sources", sn=self.sn)

    @computed_field
    @property
    def igmp_groups(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/igmp/groups", sn=self.sn)

    @computed_field
    @property
    def igmp_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/igmp/interfaces", sn=self.sn)

    @computed_field
    @property
    def igmp_snooping_global_config(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/igmp/snooping/global", sn=self.sn)

    @computed_field
    @property
    def igmp_snooping_groups(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/igmp/snooping/groups", sn=self.sn)

    @computed_field
    @property
    def igmp_snooping_vlans(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/igmp/snooping/vlans", sn=self.sn)

    @computed_field
    @property
    def mac_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/mac", sn=self.sn)

    @computed_field
    @property
    def rp_overview(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/pim/rp/overview", sn=self.sn)

    @computed_field
    @property
    def rp_bsr(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/pim/rp/bsr", sn=self.sn)

    @computed_field
    @property
    def rp_mappings(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/pim/rp/mappings", sn=self.sn)

    @computed_field
    @property
    def rp_mappings_groups(self) -> Table:
        return Table(client=self.client, endpoint="tables/multicast/pim/rp/mappings-groups", sn=self.sn)
