import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Wireless(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def controllers(self) -> Table:
        return Table(client=self.client, endpoint="tables/wireless/controllers", sn=self.sn)

    @computed_field
    @property
    def access_points(self) -> Table:
        return Table(client=self.client, endpoint="tables/wireless/access-points", sn=self.sn)

    @computed_field
    @property
    def radios_detail(self) -> Table:
        return Table(client=self.client, endpoint="tables/wireless/radio", sn=self.sn)

    @computed_field
    @property
    def radios_ssid_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/wireless/ssid-summary", sn=self.sn)

    @computed_field
    @property
    def clients(self) -> Table:
        return Table(client=self.client, endpoint="tables/wireless/clients", sn=self.sn)
