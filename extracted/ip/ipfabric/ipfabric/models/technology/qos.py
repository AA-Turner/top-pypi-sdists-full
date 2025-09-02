import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Qos(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def policy_maps(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/policy-maps", sn=self.sn)

    @computed_field
    @property
    def shaping(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/shaping", sn=self.sn)

    @computed_field
    @property
    def queuing(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/queuing", sn=self.sn)

    @computed_field
    @property
    def policing(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/policing", sn=self.sn)

    @computed_field
    @property
    def priority_queuing(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/priority-queuing", sn=self.sn)

    @computed_field
    @property
    def marking(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/marking", sn=self.sn)

    @computed_field
    @property
    def random_drops(self) -> Table:
        return Table(client=self.client, endpoint="tables/qos/random-drops", sn=self.sn)
