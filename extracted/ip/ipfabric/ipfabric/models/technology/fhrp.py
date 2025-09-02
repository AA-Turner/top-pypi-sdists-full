import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Fhrp(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def group_state(self) -> Table:
        return Table(client=self.client, endpoint="tables/fhrp/group-state", sn=self.sn)

    @computed_field
    @property
    def group_members(self) -> Table:
        return Table(client=self.client, endpoint="tables/fhrp/group-members", sn=self.sn)

    @computed_field
    @property
    def stproot_alignment(self) -> Table:
        return Table(client=self.client, endpoint="tables/fhrp/stproot-alignment", sn=self.sn)

    @computed_field
    @property
    def balancing(self) -> Table:
        return Table(client=self.client, endpoint="tables/fhrp/balancing", sn=self.sn)

    @computed_field
    @property
    def glbp_forwarders(self) -> Table:
        return Table(client=self.client, endpoint="tables/fhrp/glbp-forwarders", sn=self.sn)

    @computed_field
    @property
    def virtual_gateways(self) -> Table:
        return Table(client=self.client, endpoint="tables/fhrp/virtual-gateways", sn=self.sn)
