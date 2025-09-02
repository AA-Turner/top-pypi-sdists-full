import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class PortChannels(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def inbound_balancing_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/port-channel/balance/inbound", sn=self.sn)

    @computed_field
    @property
    def outbound_balancing_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/port-channel/balance/outbound", sn=self.sn)

    @computed_field
    @property
    def member_status_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/port-channel/member-status", sn=self.sn)

    @computed_field
    @property
    def mlag_switches(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/mlag/switches", sn=self.sn)

    @computed_field
    @property
    def mlag_peers(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/mlag/peers", sn=self.sn)

    @computed_field
    @property
    def mlag_pairs(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/mlag/pairs", sn=self.sn)

    @computed_field
    @property
    def mlag_cisco_vpc(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/mlag/vpc", sn=self.sn)
