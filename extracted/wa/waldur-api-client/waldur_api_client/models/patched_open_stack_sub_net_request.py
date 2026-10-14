from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ipv_6_mode import Ipv6Mode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_static_route_request import OpenStackStaticRouteRequest
    from ..models.open_stack_sub_net_allocation_pool_request import OpenStackSubNetAllocationPoolRequest


T = TypeVar("T", bound="PatchedOpenStackSubNetRequest")


@_attrs_define
class PatchedOpenStackSubNetRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        cidr (Union[Unset, str]):
        gateway_ip (Union[None, Unset, str]): IP address of the gateway for this subnet
        disable_gateway (Union[Unset, bool]): If True, no gateway IP address will be allocated
        allocation_pools (Union[Unset, list['OpenStackSubNetAllocationPoolRequest']]):
        ipv6_ra_mode (Union[Ipv6Mode, None, Unset]): How the router advertises an IPv6 subnet. Set at creation only;
            null for an IPv4 subnet.
        ipv6_address_mode (Union[Ipv6Mode, None, Unset]): How instances on an IPv6 subnet get their address. Set at
            creation only; null for an IPv4 subnet.
        dns_nameservers (Union[Unset, list[str]]):
        host_routes (Union[Unset, list['OpenStackStaticRouteRequest']]):
        router (Union[None, Unset, str]): Router to attach the subnet to. Optional: when omitted Waldur picks a router
            of the tenant itself. Cannot be changed here afterwards -- use the router's add/remove interface actions.
        skip_router_connection (Union[Unset, bool]): Create the subnet without attaching it to a router. Off by default,
            so an omitted field behaves exactly as before: Waldur attaches the subnet to a router of the tenant. Default:
            False.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    cidr: Union[Unset, str] = UNSET
    gateway_ip: Union[None, Unset, str] = UNSET
    disable_gateway: Union[Unset, bool] = UNSET
    allocation_pools: Union[Unset, list["OpenStackSubNetAllocationPoolRequest"]] = UNSET
    ipv6_ra_mode: Union[Ipv6Mode, None, Unset] = UNSET
    ipv6_address_mode: Union[Ipv6Mode, None, Unset] = UNSET
    dns_nameservers: Union[Unset, list[str]] = UNSET
    host_routes: Union[Unset, list["OpenStackStaticRouteRequest"]] = UNSET
    router: Union[None, Unset, str] = UNSET
    skip_router_connection: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        cidr = self.cidr

        gateway_ip: Union[None, Unset, str]
        if isinstance(self.gateway_ip, Unset):
            gateway_ip = UNSET
        else:
            gateway_ip = self.gateway_ip

        disable_gateway = self.disable_gateway

        allocation_pools: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.allocation_pools, Unset):
            allocation_pools = []
            for allocation_pools_item_data in self.allocation_pools:
                allocation_pools_item = allocation_pools_item_data.to_dict()
                allocation_pools.append(allocation_pools_item)

        ipv6_ra_mode: Union[None, Unset, str]
        if isinstance(self.ipv6_ra_mode, Unset):
            ipv6_ra_mode = UNSET
        elif isinstance(self.ipv6_ra_mode, Ipv6Mode):
            ipv6_ra_mode = self.ipv6_ra_mode.value
        else:
            ipv6_ra_mode = self.ipv6_ra_mode

        ipv6_address_mode: Union[None, Unset, str]
        if isinstance(self.ipv6_address_mode, Unset):
            ipv6_address_mode = UNSET
        elif isinstance(self.ipv6_address_mode, Ipv6Mode):
            ipv6_address_mode = self.ipv6_address_mode.value
        else:
            ipv6_address_mode = self.ipv6_address_mode

        dns_nameservers: Union[Unset, list[str]] = UNSET
        if not isinstance(self.dns_nameservers, Unset):
            dns_nameservers = []
            for dns_nameservers_item_data in self.dns_nameservers:
                dns_nameservers_item: str
                dns_nameservers_item = dns_nameservers_item_data
                dns_nameservers.append(dns_nameservers_item)

        host_routes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.host_routes, Unset):
            host_routes = []
            for host_routes_item_data in self.host_routes:
                host_routes_item = host_routes_item_data.to_dict()
                host_routes.append(host_routes_item)

        router: Union[None, Unset, str]
        if isinstance(self.router, Unset):
            router = UNSET
        else:
            router = self.router

        skip_router_connection = self.skip_router_connection

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if cidr is not UNSET:
            field_dict["cidr"] = cidr
        if gateway_ip is not UNSET:
            field_dict["gateway_ip"] = gateway_ip
        if disable_gateway is not UNSET:
            field_dict["disable_gateway"] = disable_gateway
        if allocation_pools is not UNSET:
            field_dict["allocation_pools"] = allocation_pools
        if ipv6_ra_mode is not UNSET:
            field_dict["ipv6_ra_mode"] = ipv6_ra_mode
        if ipv6_address_mode is not UNSET:
            field_dict["ipv6_address_mode"] = ipv6_address_mode
        if dns_nameservers is not UNSET:
            field_dict["dns_nameservers"] = dns_nameservers
        if host_routes is not UNSET:
            field_dict["host_routes"] = host_routes
        if router is not UNSET:
            field_dict["router"] = router
        if skip_router_connection is not UNSET:
            field_dict["skip_router_connection"] = skip_router_connection

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_static_route_request import OpenStackStaticRouteRequest
        from ..models.open_stack_sub_net_allocation_pool_request import OpenStackSubNetAllocationPoolRequest

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        cidr = d.pop("cidr", UNSET)

        def _parse_gateway_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gateway_ip = _parse_gateway_ip(d.pop("gateway_ip", UNSET))

        disable_gateway = d.pop("disable_gateway", UNSET)

        allocation_pools = []
        _allocation_pools = d.pop("allocation_pools", UNSET)
        for allocation_pools_item_data in _allocation_pools or []:
            allocation_pools_item = OpenStackSubNetAllocationPoolRequest.from_dict(allocation_pools_item_data)

            allocation_pools.append(allocation_pools_item)

        def _parse_ipv6_ra_mode(data: object) -> Union[Ipv6Mode, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ipv6_ra_mode_type_0 = Ipv6Mode(data)

                return ipv6_ra_mode_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Ipv6Mode, None, Unset], data)

        ipv6_ra_mode = _parse_ipv6_ra_mode(d.pop("ipv6_ra_mode", UNSET))

        def _parse_ipv6_address_mode(data: object) -> Union[Ipv6Mode, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ipv6_address_mode_type_0 = Ipv6Mode(data)

                return ipv6_address_mode_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Ipv6Mode, None, Unset], data)

        ipv6_address_mode = _parse_ipv6_address_mode(d.pop("ipv6_address_mode", UNSET))

        dns_nameservers = []
        _dns_nameservers = d.pop("dns_nameservers", UNSET)
        for dns_nameservers_item_data in _dns_nameservers or []:

            def _parse_dns_nameservers_item(data: object) -> str:
                return cast(str, data)

            dns_nameservers_item = _parse_dns_nameservers_item(dns_nameservers_item_data)

            dns_nameservers.append(dns_nameservers_item)

        host_routes = []
        _host_routes = d.pop("host_routes", UNSET)
        for host_routes_item_data in _host_routes or []:
            host_routes_item = OpenStackStaticRouteRequest.from_dict(host_routes_item_data)

            host_routes.append(host_routes_item)

        def _parse_router(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        router = _parse_router(d.pop("router", UNSET))

        skip_router_connection = d.pop("skip_router_connection", UNSET)

        patched_open_stack_sub_net_request = cls(
            name=name,
            description=description,
            cidr=cidr,
            gateway_ip=gateway_ip,
            disable_gateway=disable_gateway,
            allocation_pools=allocation_pools,
            ipv6_ra_mode=ipv6_ra_mode,
            ipv6_address_mode=ipv6_address_mode,
            dns_nameservers=dns_nameservers,
            host_routes=host_routes,
            router=router,
            skip_router_connection=skip_router_connection,
        )

        patched_open_stack_sub_net_request.additional_properties = d
        return patched_open_stack_sub_net_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
