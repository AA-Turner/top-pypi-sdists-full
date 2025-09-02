import json
import logging
from collections import OrderedDict
from ipaddress import (
    ip_interface,
    ip_address,
    IPv4Address,
    IPv6Address,
    IPv4Interface,
    IPv6Interface,
)
from typing import Any, Union, Literal

from macaddress import EUI48
from pydantic import BaseModel, Field, PrivateAttr

from ipfabric.models.oas import Endpoint, NestedColumn, Column
from ipfabric.tools.shared import parse_mac

LOGGER = logging.getLogger("ipfabric")

VM_INTS = "/tables/cloud/endpoints/virtual-machines-interfaces"
SEARCH_PATHS_IGNORE = [
    "/tables/networks",  # Deprecated
    "/tables/networks/ipv6-routes",  # Route tables match too many items
    "/tables/networks/routes",
    "/tables/mpls/l3-vpn/pe-routes",
    "/tables/routing/protocols/lisp/ipv4-routes",
    "/tables/mpls/forwarding",
    "/tables/addressing/path-lookup-sources",
    "/tables/addressing/path-lookup-sources-multicast",
    "/tables/addressing/path-lookup-sources-unicast",
    "/tables/management/changes/managed-devs",
    "/tables/reports/discovery-tasks",
    "/tables/interfaces/connectivity-matrix/unmanaged-neighbors/summary",  # Summary table
    "/tables/routing/protocols/bgp/address-families",
    "/tables/routing/protocols/ospf/interfaces",
    "/tables/routing/protocols/ospf-v3/interfaces",
    "/tables/management/connectivity-errors",
    "/tables/settings/jumphosts",
    "/tables/settings/ports",
    "/tables/networks/route-stability",
    "/tables/networks/gateway-redundancy",
]
RANKED = {
    "ipv4": [
        "/tables/addressing/managed-devs",
        "/tables/inventory/interfaces",
        "/tables/addressing/hosts",
        "/tables/addressing/arp",
        "/tables/addressing/ipv4-managed-ip-summary",
        "/tables/wireless/clients",
        "/tables/inventory/phones",
        VM_INTS,
        "/tables/neighbors/unmanaged",
        "/tables/interfaces/connectivity-matrix/unmanaged-neighbors/detail",
        "/tables/routing/protocols/bgp/neighbors",
        "/tables/routing/protocols/eigrp/neighbors",
        "/tables/routing/protocols/is-is/neighbors",
        "/tables/routing/protocols/ospf/neighbors",
        "/tables/routing/protocols/rip/neighbors",
    ],
    "ipv6": [
        "/tables/addressing/ipv6-managed-devs",
        "/tables/addressing/ipv6-hosts",
        "/tables/addressing/ipv6-neighbors",
        "/tables/neighbors/unmanaged",
        "/tables/interfaces/connectivity-matrix/unmanaged-neighbors/detail",
        VM_INTS,
        "/tables/routing/protocols/bgp/neighbors",
        "/tables/routing/protocols/is-is/neighbors",
        "/tables/routing/protocols/ospf-v3/neighbors",  # NIM-15216
    ],
    "mac": [
        "/tables/addressing/managed-devs",
        "/tables/addressing/ipv6-managed-devs",
        "/tables/inventory/interfaces",
        "/tables/addressing/hosts",
        "/tables/addressing/ipv6-hosts",
        "/tables/addressing/ipv6-neighbors",
        "/tables/addressing/arp",
        VM_INTS,
        "/tables/addressing/mac",
        "/tables/wireless/radio",
    ],
}
OPERATORS = {
    "CIDR": "cidr",
    "=": "eq",
    "IP": "ip",
    ">": "gt",
    ">=": "gte",
    "<": "lt",
    "<=": "lte",
    "@": "sect",
    "!@": "nsect",
}
VALID_OPS = Literal[
    "=", "IP", ">", ">=", "<", "<=", "@", "!@", "eq", "ip", "gt", "gte", "lt", "lte", "sect", "nsect", "cidr", "CIDR"
]
IP_ADDRESS = (IPv4Address, IPv6Address)
IP_INTERFACE = (IPv4Interface, IPv6Interface)


class GlobalSearch(BaseModel):
    client: Any = Field(exclude=True)
    _ipv4: list[Endpoint] = PrivateAttr(default_factory=list)
    _ipv6: list[Endpoint] = PrivateAttr(default_factory=list)
    _mac: list[Endpoint] = PrivateAttr(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        self._load_default()
        self._load_dynamic()

    def _load_default(self):
        for k, v in RANKED.items():
            for path in v:
                if getattr(self.client.oas[path[1:]].post, k).columns:
                    getattr(self.client.oas[path[1:]].post, k).full_scan = False
                    getattr(self, k).append(self.client.oas[path[1:]].post)

    def _load_dynamic(self):
        for path in self.client.oas.values():
            if path.post:
                if path.full_api_endpoint in SEARCH_PATHS_IGNORE:
                    continue
                for k, paths in RANKED.items():
                    if path.full_api_endpoint not in paths and getattr(path.post, k).columns:
                        getattr(self, k).append(path.post)

    @property
    def ipv4(self):
        return self._ipv4

    @property
    def ipv6(self):
        return self._ipv6

    @property
    def mac(self):
        return self._mac

    @staticmethod
    def _create_filter(
        columns: list[Union[Column, NestedColumn]], path: Endpoint, value: str, regex: bool = False
    ) -> dict:
        oper = "reg" if regex else "eq"
        filters = [
            (
                {col.parent: ["any", col.child, oper, value]}
                if isinstance(col, NestedColumn)
                else {col.name: ["any", oper, value]} if col.name in path.array_columns else {col.name: [oper, value]}
            )
            for col in columns
            if not getattr(col, "filter", "").startswith("routing")
        ]
        return {"or": filters} if filters else None

    def _search(
        self,
        search_type: Literal["ipv4", "ipv6", "mac"],
        address: str,
        full_scan: bool = False,
        regex: bool = False,
        first_match: bool = False,
    ) -> dict[str, dict[str, Union[str, list]]]:

        results, data = OrderedDict(), list()

        for path in getattr(self, search_type):
            search_data = getattr(path, search_type)
            if first_match and data:
                LOGGER.debug("Found first match, stopping search.")
                break
            elif not full_scan and search_data.full_scan is True:
                LOGGER.debug('Finished searching default tables; "--full-scan" not enabled to search all tables.')
                break  # List is ordered and once this is met we can break if not full scan
            filters = self._create_filter(search_data.columns, path, address, True if regex else False)
            if not filters:
                continue
            msg = f'earching "{path.web_menu}": API Endpoint: "{path.full_api_endpoint}"'
            LOGGER.debug(f'S{msg}; Filters `{json.dumps(filters, separators=(",", ":"))}`.')
            data = self.client.fetch_all(path.api_endpoint, filters=filters)
            results[path.full_api_endpoint] = {
                "data": data,
                "path": path.full_api_endpoint,
                "webPath": path.web_endpoint,
                "url": path.filter_url(filters, self.client._client.base_url),
                "menu": f'{path.web_menu}: "{path.title or path.summary}"',
            }
            LOGGER.debug(f"Finished s{msg}.")

        return results

    def search(
        self,
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> Union[None, dict[str, dict[str, Union[str, list]]]]:

        if isinstance(address, int):
            raise TypeError(f"Input must be a valid string not integer: {str(address)}")
        try:
            return self.search_mac(address, full_scan, first_match)
        except ValueError:
            pass
        try:
            return self.search_ip(address, full_scan, first_match)
        except ValueError:
            raise SyntaxError(f'Address does not appear to be a IPv4, IPv6, nor MAC Address: "{address}".')

    def search_mac(
        self,
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> dict[str, dict[str, Union[str, list]]]:

        if isinstance(address, int):
            raise TypeError(f"Input must be a valid string not integer: {str(address)}")
        LOGGER.info("Verifying Address is a MAC.")
        EUI48(address)
        mac = parse_mac(address)
        LOGGER.debug(f'Searching for MAC Address "{mac}".')
        return self._search("mac", mac, full_scan, first_match=first_match)

    def search_ip(
        self,
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> dict[str, dict[str, Union[str, list]]]:
        LOGGER.info("Verifying Address is an IP.")
        ip = ip_address(address)
        if ip.version == 4:
            LOGGER.debug(f'Searching for IPv4 Address "{str(ip)}".')
            return self._search("ipv4", str(ip), full_scan, first_match=first_match)
        elif ip.version == 6:
            LOGGER.debug(f'Searching for IPv6 Address "{str(ip)}".')
            return self._search("ipv6", str(ip), full_scan, first_match=first_match)

    def _search_ip(
        self,
        version: int,
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> dict[str, dict[str, Union[str, list]]]:
        ip = ip_address(address)
        if ip.version != version:
            raise ValueError()
        return self._search("ipv" + str(version), str(ip), full_scan, first_match=first_match)

    def search_ipv4(
        self,
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> Union[None, dict[str, dict[str, Union[str, list]]]]:
        return self._search_ip(4, address, full_scan, first_match)

    def search_ipv6(
        self,
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> Union[None, dict[str, dict[str, Union[str, list]]]]:
        return self._search_ip(6, address, full_scan, first_match)

    def search_regex(
        self,
        search_type: Literal["ipv4", "ipv6", "mac"],
        address: str,
        full_scan: bool = False,
        first_match: bool = False,
    ) -> dict[str, dict[str, Union[str, list]]]:
        LOGGER.debug(f'Searching for {search_type.upper()} Address "{address}".')
        return self._search(search_type, address, full_scan, True, first_match)


class RouteTableSearch(BaseModel):
    client: Any = Field(exclude=True)
    _route: str = "tables/networks/routes"
    _route6: str = "tables/networks/ipv6-routes"

    @staticmethod
    def _check_ip(address: str) -> Union[IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]:
        try:
            return ip_address(address)
        except ValueError:
            LOGGER.debug(f'Address "{address}" is not IP Address, trying as subnet.')
            try:
                return ip_interface(address)
            except ValueError:
                raise SyntaxError(f'Address does not appear to be a IPv4 or IPv6 Address/Subnet: "{address}".')

    @staticmethod
    def _check_search(  # NOSONAR
        ip: Union[IPv4Address, IPv6Address, IPv4Interface, IPv6Interface],
        operator: str,
        next_hop: bool = False,
    ) -> Union[IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]:
        if next_hop:
            if operator not in ["cidr", "eq"]:
                raise SyntaxError("IP, EQ, or CIDR search only allowed for Next Hop IP.")
            elif isinstance(ip, IP_INTERFACE) and operator == "eq":
                ip = ip.ip
        else:
            if ip.version == 6 and operator not in ["ip", "eq"]:
                raise SyntaxError('IPv6 CIDR Search not implemented yet, please use "ip" or "eq".')  # NIM-14175
            elif operator == "cidr":
                raise SyntaxError('"CIDR" Search only used in Next Hop IP.')
            elif isinstance(ip, IP_INTERFACE) and operator == "ip" and ip.max_prefixlen != ip.network.prefixlen:
                raise SyntaxError(f'IP Search must be IP not CIDR: "{str(ip)}".')
            elif isinstance(ip, IP_ADDRESS) and operator != "ip":
                ip = ip_interface(str(ip))
            elif isinstance(ip, IP_INTERFACE) and operator == "ip":
                ip = ip.ip
        return ip

    def search(
        self, address: str, operator: VALID_OPS = "=", next_hop: bool = False, ignore_default: bool = True
    ) -> dict[str, Any]:
        """ """
        if operator not in OPERATORS.values():
            operator = OPERATORS[operator]
        operator = "eq" if operator == "ip" and next_hop else operator
        ip = self._check_search(self._check_ip(address), operator, next_hop)

        filters = {"nexthop": ["any", "ip", operator, str(ip)]} if next_hop else {"network": [operator, str(ip)]}
        if ignore_default and str(ip) not in ["0.0.0.0/0", "::/0"]:
            filters = {"and": [filters, {"network": ["neq", "0.0.0.0/0" if ip.version == 4 else "::/0"]}]}
        api_endpoint = self._route if ip.version == 4 else self._route6
        path = self.client.oas[api_endpoint].post
        return {
            "data": self.client.fetch_all(url=api_endpoint, filters=filters),
            "path": path.full_api_endpoint,
            "webPath": path.web_endpoint,
            "url": path.filter_url(filters, self.client._client.base_url),
            "menu": f'{path.web_menu}: "{path.title or path.summary}"',
        }
