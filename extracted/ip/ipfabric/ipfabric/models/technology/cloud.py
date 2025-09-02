import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Cloud(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def virtual_machines(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/endpoints/virtual-machines", sn=self.sn)

    @computed_field
    @property
    def virtual_machines_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/endpoints/virtual-machines-interfaces", sn=self.sn)

    @computed_field
    @property
    def aws_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/aws/inventory", sn=self.sn)

    @computed_field
    @property
    def azure_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/azure/inventory", sn=self.sn)

    @computed_field
    @property
    def gcp_inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/vendors/gcp/inventory", sn=self.sn)

    @computed_field
    @property
    def inventory(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/nodes/inventory", sn=self.sn)

    @computed_field
    @property
    def tags(self) -> Table:
        return Table(client=self.client, endpoint="tables/cloud/nodes/tags", sn=self.sn)
