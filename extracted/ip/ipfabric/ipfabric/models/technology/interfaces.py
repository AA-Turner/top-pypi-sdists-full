import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Interfaces(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def current_rates_data_inbound(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/load/inbound", sn=self.sn)

    @computed_field
    @property
    def current_rates_data_outbound(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/load/outbound", sn=self.sn)

    @computed_field
    @property
    def current_rates_data_bidirectional(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/load/bidirectional", sn=self.sn)

    @computed_field
    @property
    def duplex(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/duplex", sn=self.sn)

    @computed_field
    @property
    def err_disabled(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/errors/disabled", sn=self.sn)

    @computed_field
    @property
    def connectivity_matrix(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/connectivity-matrix", sn=self.sn)

    @computed_field
    @property
    def connectivity_matrix_unmanaged_neighbors_summary(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/interfaces/connectivity-matrix/unmanaged-neighbors/summary", sn=self.sn
        )

    @computed_field
    @property
    def connectivity_matrix_unmanaged_neighbors_detail(self) -> Table:
        return Table(
            client=self.client, endpoint="tables/interfaces/connectivity-matrix/unmanaged-neighbors/detail", sn=self.sn
        )

    @computed_field
    @property
    def switchport(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/switchports", sn=self.sn)

    @computed_field
    @property
    def mtu(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/mtu", sn=self.sn)

    @computed_field
    @property
    def storm_control_all(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/storm-control/all", sn=self.sn)

    @computed_field
    @property
    def storm_control_broadcast(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/storm-control/broadcast", sn=self.sn)

    @computed_field
    @property
    def storm_control_unicast(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/storm-control/unicast", sn=self.sn)

    @computed_field
    @property
    def storm_control_multicast(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/storm-control/multicast", sn=self.sn)

    @computed_field
    @property
    def transceivers(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/transceivers/inventory", sn=self.sn)

    @computed_field
    @property
    def transceivers_statistics(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/transceivers/statistics", sn=self.sn)

    @computed_field
    @property
    def transceivers_triggered_thresholds(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/transceivers/thresholds", sn=self.sn)

    @computed_field
    @property
    def transceivers_errors(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/transceivers/errors", sn=self.sn)

    @computed_field
    @property
    def point_to_point_over_ethernet(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/pppoe", sn=self.sn)

    @computed_field
    @property
    def point_to_point_over_ethernet_sessions(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/pppoe/sessions", sn=self.sn)

    @computed_field
    @property
    def counters_inbound(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/counters/inbound", sn=self.sn)

    @computed_field
    @property
    def counters_outbound(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/counters/outbound", sn=self.sn)

    @computed_field
    @property
    def tunnels_ipv4(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/tunnels/ipv4", sn=self.sn)

    @computed_field
    @property
    def tunnels_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/tunnels/ipv6", sn=self.sn)

    @computed_field
    @property
    def virtual_wires(self) -> Table:
        return Table(client=self.client, endpoint="tables/interfaces/virtual-wires", sn=self.sn)
