import logging
from typing import Any, Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric.models.table import Table

logger = logging.getLogger("ipfabric")


class Routing(BaseModel):
    client: Any = Field(None, exclude=True)
    sn: Optional[str] = None

    def print_tables(self):
        print(sorted([_ for _ in dir(self) if _[0] != "_" and isinstance(getattr(self, _), Table)]))

    @computed_field
    @property
    def summary_protocols(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols", sn=self.sn)

    @computed_field
    @property
    def summary_protocols_bgp(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols/bgp", sn=self.sn)

    @computed_field
    @property
    def summary_protocols_eigrp(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols/eigrp", sn=self.sn)

    @computed_field
    @property
    def summary_protocols_isis(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols/isis", sn=self.sn)

    @computed_field
    @property
    def summary_protocols_ospf(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols/ospf", sn=self.sn)

    @computed_field
    @property
    def summary_protocols_ospfv3(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols/ospfv3", sn=self.sn)

    @computed_field
    @property
    def summary_protocols_rip(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/summary/protocols/rip", sn=self.sn)

    @computed_field
    @property
    def routes_ipv4(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/routes", sn=self.sn)

    @computed_field
    @property
    def routes_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/ipv6-routes", sn=self.sn)

    @computed_field
    @property
    def route_stability(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/route-stability", sn=self.sn)

    @computed_field
    @property
    def ospf_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/ospf/neighbors", sn=self.sn)

    @computed_field
    @property
    def ospf_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/ospf/interfaces", sn=self.sn)

    @computed_field
    @property
    def ospfv3_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/ospf-v3/neighbors", sn=self.sn)

    @computed_field
    @property
    def ospfv3_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/ospf-v3/interfaces", sn=self.sn)

    @computed_field
    @property
    def bgp_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/bgp/neighbors", sn=self.sn)

    @computed_field
    @property
    def bgp_address_families(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/bgp/address-families", sn=self.sn)

    @computed_field
    @property
    def bgp_routes(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/bgp/routes", sn=self.sn)

    @computed_field
    @property
    def eigrp_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/eigrp/neighbors", sn=self.sn)

    @computed_field
    @property
    def eigrp_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/eigrp/interfaces", sn=self.sn)

    @computed_field
    @property
    def rip_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/rip/neighbors", sn=self.sn)

    @computed_field
    @property
    def rip_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/rip/interfaces", sn=self.sn)

    @computed_field
    @property
    def isis_neighbors(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/is-is/neighbors", sn=self.sn)

    @computed_field
    @property
    def isis_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/is-is/interfaces", sn=self.sn)

    @computed_field
    @property
    def isis_levels(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/is-is/levels", sn=self.sn)

    @computed_field
    @property
    def path_lookup_checks(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/path-lookup-checks", sn=self.sn)

    @computed_field
    @property
    def vrf_summary(self) -> Table:
        return Table(client=self.client, endpoint="tables/vrf/summary", sn=self.sn)

    @computed_field
    @property
    def vrf_detail(self) -> Table:
        return Table(client=self.client, endpoint="tables/vrf/detail", sn=self.sn)

    @computed_field
    @property
    def vrf_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/vrf/interfaces", sn=self.sn)

    @computed_field
    @property
    def policies_prefix_list(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/policies/prefix-lists/ipv4", sn=self.sn)

    @computed_field
    @property
    def policies_prefix_list_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/policies/prefix-lists/ipv6", sn=self.sn)

    @computed_field
    @property
    def lisp_routes_ipv4(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/lisp/ipv4-routes", sn=self.sn)

    @computed_field
    @property
    def lisp_routes_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/lisp/ipv6-routes", sn=self.sn)

    @computed_field
    @property
    def lisp_map_resolvers_ipv4(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/lisp/ipv4-databases", sn=self.sn)

    @computed_field
    @property
    def lisp_map_resolvers_ipv6(self) -> Table:
        return Table(client=self.client, endpoint="tables/routing/protocols/lisp/ipv6-databases", sn=self.sn)

    @computed_field
    @property
    def policies(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/policies/routing", sn=self.sn)

    @computed_field
    @property
    def policies_interfaces(self) -> Table:
        return Table(client=self.client, endpoint="tables/networks/policies/routing/interfaces", sn=self.sn)

    @computed_field
    @property
    def policies_pbr(self) -> Table:
        return Table(client=self.client, endpoint="tables/security/pbr", sn=self.sn)
