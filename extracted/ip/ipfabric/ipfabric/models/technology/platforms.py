import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Platforms(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def environment_power_supplies(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/power-supplies", sn=self.sn)

    @computed_field
    @property
    def environment_power_supplies_fans(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/power-supplies-fans", sn=self.sn)

    @computed_field
    @property
    def environment_fans(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/fans", sn=self.sn)

    @computed_field
    @property
    def environment_modules(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/modules", sn=self.sn)

    @computed_field
    @property
    def environment_temperature_sensors(self) -> Table:
        return Table(client=self.client, endpoint="tables/inventory/temperature-sensors", sn=self.sn)

    @computed_field
    @property
    def cisco_fabric_path_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/fabric-path/summary", sn=self.sn)

    @computed_field
    @property
    def cisco_fabric_path_isis_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/fabric-path/neighbors", sn=self.sn)

    @computed_field
    @property
    def cisco_fabric_path_switches(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/fabric-path/switches", sn=self.sn)

    @computed_field
    @property
    def cisco_fabric_path_routes(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/fabric-path/routes", sn=self.sn)

    @computed_field
    @property
    def juniper_cluster(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/cluster/srx", sn=self.sn)

    @computed_field
    @property
    def cisco_fex_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/fex/interfaces", sn=self.sn)

    @computed_field
    @property
    def cisco_fex_modules(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/fex/modules", sn=self.sn)

    @computed_field
    @property
    def cisco_vdc_devices(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/vdc/devices", sn=self.sn)

    @computed_field
    @property
    def platform_cisco_vss(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/vss/overview", sn=self.sn)

    @computed_field
    @property
    def cisco_vss_chassis(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/vss/chassis", sn=self.sn)

    @computed_field
    @property
    def cisco_vss_vsl(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/vss/vsl", sn=self.sn)

    @computed_field
    @property
    def poe_devices(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/poe/devices", sn=self.sn)

    @computed_field
    @property
    def poe_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/poe/interfaces", sn=self.sn)

    @computed_field
    @property
    def poe_modules(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/poe/modules", sn=self.sn)

    @computed_field
    @property
    def stacks(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/stack", sn=self.sn)

    @computed_field
    @property
    def stacks_members(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/stack/members", sn=self.sn)

    @computed_field
    @property
    def stacks_stack_ports(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/stack/connections", sn=self.sn)

    @computed_field
    @property
    def logical_devices(self) -> Table:
        return Table(client=self.client, endpoint="tables/platforms/devices", sn=self.sn)
