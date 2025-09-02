import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Addressing(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def arp_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/arp", sn=self.sn)

    @computed_field
    @property
    def mac_table(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/mac", sn=self.sn)

    @computed_field
    @property
    def managed_ipv4_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/ipv4-managed-ip-summary", sn=self.sn)

    @computed_field
    @property
    def managed_ip_ipv4(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/managed-devs", sn=self.sn)

    @computed_field
    @property
    def managed_ip_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/ipv6-managed-devs", sn=self.sn)

    @computed_field
    @property
    def managed_duplicate_ip(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/duplicate-ip", sn=self.sn)

    @computed_field
    @property
    def nat44(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/nat44", sn=self.sn)

    @computed_field
    @property
    def ipv6_neighbor_discovery(self) -> Table:
        return Table(client=self.client, endpoint="tables/addressing/ipv6-neighbors", sn=self.sn)
