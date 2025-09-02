import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Mpls(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def ldp_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/ldp/neighbors", sn=self.sn)

    @computed_field
    @property
    def ldp_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/ldp/interfaces", sn=self.sn)

    @computed_field
    @property
    def rsvp_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/rsvp/neighbors", sn=self.sn)

    @computed_field
    @property
    def rsvp_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/rsvp/interfaces", sn=self.sn)

    @computed_field
    @property
    def forwarding(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/forwarding", sn=self.sn)

    @computed_field
    @property
    def l3vpn_pe_routers(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l3-vpn/pe-routers", sn=self.sn)

    @computed_field
    @property
    def l3vpn_pe_vrfs(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l3-vpn/pe-vrfs", sn=self.sn)

    @computed_field
    @property
    def l3vpn_vrf_targets(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l3-vpn/vrf-targets", sn=self.sn)

    @computed_field
    @property
    def l3vpn_pe_routes(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l3-vpn/pe-routes", sn=self.sn)

    @computed_field
    @property
    def l2vpn_point_to_point_vpws(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l2-vpn/point-to-point-vpws", sn=self.sn)

    @computed_field
    @property
    def l2vpn_point_to_multipoint(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l2-vpn/point-to-multipoint", sn=self.sn)

    @computed_field
    @property
    def l2vpn_circuit_cross_connect(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l2-vpn/circuit-cross-connect", sn=self.sn)

    @computed_field
    @property
    def l2vpn_pseudowires(self) -> Table:
        return Table(client=self.client, endpoint="tables/mpls/l2-vpn/pseudowires", sn=self.sn)
