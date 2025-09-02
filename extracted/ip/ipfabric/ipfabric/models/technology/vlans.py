import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Vlans(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def device_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/vlan/device-summary", sn=self.sn)

    @computed_field
    @property
    def device_detail(self) -> Table:
        return Table(client=self.client, endpoint="tables/vlan/device", sn=self.sn)

    @computed_field
    @property
    def network_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/vlan/network-summary", sn=self.sn)

    @computed_field
    @property
    def site_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/vlan/site-summary", sn=self.sn)

    @computed_field
    @property
    def l3_gateways(self) -> Table:
        return Table(client=self.client, endpoint="tables/vlan/l3-gateways", sn=self.sn)
