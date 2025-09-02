import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Dhcp(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def relay_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/interfaces", sn=self.sn)

    @computed_field
    @property
    def relay_interfaces_stats_received(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/interfaces-stats/received", sn=self.sn)

    @computed_field
    @property
    def relay_interfaces_stats_relayed(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/interfaces-stats/relayed", sn=self.sn)

    @computed_field
    @property
    def relay_interfaces_stats_sent(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/interfaces-stats/sent", sn=self.sn)

    @computed_field
    @property
    def relay_global_stats_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/summary", sn=self.sn)

    @computed_field
    @property
    def relay_global_stats_received(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/received", sn=self.sn)

    @computed_field
    @property
    def relay_global_stats_relayed(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/relayed", sn=self.sn)

    @computed_field
    @property
    def relay_global_stats_sent(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/relay/global-stats/sent", sn=self.sn)

    @computed_field
    @property
    def server_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/server/summary", sn=self.sn)

    @computed_field
    @property
    def server_pools(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/server/pools", sn=self.sn)

    @computed_field
    @property
    def server_leases(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/server/leases", sn=self.sn)

    @computed_field
    @property
    def server_excluded_ranges(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/server/excluded-ranges", sn=self.sn)

    @computed_field
    @property
    def server_excluded_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/dhcp/server/interfaces", sn=self.sn)
