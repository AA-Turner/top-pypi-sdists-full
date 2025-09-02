import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class LoadBalancing(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def virtual_servers(self) -> Table:
        return Table(client=self.client, endpoint="tables/load-balancing/virtual-servers", sn=self.sn)

    @computed_field
    @property
    def virtual_servers_pools(self) -> Table:
        return Table(client=self.client, endpoint="tables/load-balancing/virtual-servers/pools", sn=self.sn)

    @computed_field
    @property
    def virtual_servers_pool_members(self) -> Table:
        return Table(client=self.client, endpoint="tables/load-balancing/virtual-servers/pool-members", sn=self.sn)

    @computed_field
    @property
    def partitions(self) -> Table:
        return Table(client=self.client, endpoint="tables/load-balancing/partitions", sn=self.sn)
