import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Sdwan(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def versa_sites(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/versa/sites", sn=self.sn)

    @computed_field
    @property
    def versa_links(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/versa/links", sn=self.sn)

    @computed_field
    @property
    def silverpeak_overlay(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/silverpeak/overlay", sn=self.sn)

    @computed_field
    @property
    def silverpeak_underlay(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/silverpeak/underlay", sn=self.sn)

    @computed_field
    @property
    def viptela_bfd_sessions(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/viptela/bfd-sessions", sn=self.sn)

    @computed_field
    @property
    def viptela_bfd_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/viptela/bfd-summary", sn=self.sn)

    @computed_field
    @property
    def viptela_control_connections(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/viptela/control-connections", sn=self.sn)

    @computed_field
    @property
    def velocloud_overlay(self) -> Table:
        return Table(client=self.client, endpoint="tables/sdwan/velocloud/overlay", sn=self.sn)
