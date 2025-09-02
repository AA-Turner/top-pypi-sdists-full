import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Neighbors(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def neighbors_all(self) -> Table:
        return Table(client=self.client, endpoint="tables/neighbors/all", sn=self.sn)

    @computed_field
    @property
    def neighbors_unmanaged(self) -> Table:
        return Table(client=self.client, endpoint="tables/neighbors/unmanaged", sn=self.sn)

    @computed_field
    @property
    def neighbors_unidirectional(self) -> Table:
        return Table(client=self.client, endpoint="tables/neighbors/unidirectional", sn=self.sn)

    @computed_field
    @property
    def neighbors_endpoints(self) -> Table:
        return Table(client=self.client, endpoint="tables/neighbors/endpoints", sn=self.sn)
