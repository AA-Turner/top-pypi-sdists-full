import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Oam(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def unidirectional_link_detection_neighbors(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/management/oam/unidirectional-link-detection/neighbors", sn=self.sn
        )

    @computed_field
    @property
    def unidirectional_link_detection_interfaces(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/management/oam/unidirectional-link-detection/interfaces", sn=self.sn
        )
