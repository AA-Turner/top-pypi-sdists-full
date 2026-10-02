from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.effective_route_source_enum import EffectiveRouteSourceEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="EffectiveRoute")


@_attrs_define
class EffectiveRoute:
    """
    Attributes:
        destination (str):
        nexthop (Union[None, str]): An IPv4 or IPv6 address.
        source (EffectiveRouteSourceEnum):
        subnet_uuid (Union[None, Unset, str]):
        subnet_name (Union[Unset, str]):
        subnet_cidr (Union[Unset, str]):
        port_uuid (Union[None, Unset, str]):
        port_backend_id (Union[Unset, str]):
        ip_on_router (Union[None, Unset, str]): An IPv4 or IPv6 address.
        gateway_ip_on_router (Union[None, Unset, str]): An IPv4 or IPv6 address.
        external_network_uuid (Union[None, Unset, str]):
        external_network_name (Union[Unset, str]):
    """

    destination: str
    nexthop: Union[None, str]
    source: EffectiveRouteSourceEnum
    subnet_uuid: Union[None, Unset, str] = UNSET
    subnet_name: Union[Unset, str] = UNSET
    subnet_cidr: Union[Unset, str] = UNSET
    port_uuid: Union[None, Unset, str] = UNSET
    port_backend_id: Union[Unset, str] = UNSET
    ip_on_router: Union[None, Unset, str] = UNSET
    gateway_ip_on_router: Union[None, Unset, str] = UNSET
    external_network_uuid: Union[None, Unset, str] = UNSET
    external_network_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        destination = self.destination

        nexthop: Union[None, str]
        nexthop = self.nexthop

        source = self.source.value

        subnet_uuid: Union[None, Unset, str]
        if isinstance(self.subnet_uuid, Unset):
            subnet_uuid = UNSET
        else:
            subnet_uuid = self.subnet_uuid

        subnet_name = self.subnet_name

        subnet_cidr = self.subnet_cidr

        port_uuid: Union[None, Unset, str]
        if isinstance(self.port_uuid, Unset):
            port_uuid = UNSET
        else:
            port_uuid = self.port_uuid

        port_backend_id = self.port_backend_id

        ip_on_router: Union[None, Unset, str]
        if isinstance(self.ip_on_router, Unset):
            ip_on_router = UNSET
        else:
            ip_on_router = self.ip_on_router

        gateway_ip_on_router: Union[None, Unset, str]
        if isinstance(self.gateway_ip_on_router, Unset):
            gateway_ip_on_router = UNSET
        else:
            gateway_ip_on_router = self.gateway_ip_on_router

        external_network_uuid: Union[None, Unset, str]
        if isinstance(self.external_network_uuid, Unset):
            external_network_uuid = UNSET
        else:
            external_network_uuid = self.external_network_uuid

        external_network_name = self.external_network_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "destination": destination,
                "nexthop": nexthop,
                "source": source,
            }
        )
        if subnet_uuid is not UNSET:
            field_dict["subnet_uuid"] = subnet_uuid
        if subnet_name is not UNSET:
            field_dict["subnet_name"] = subnet_name
        if subnet_cidr is not UNSET:
            field_dict["subnet_cidr"] = subnet_cidr
        if port_uuid is not UNSET:
            field_dict["port_uuid"] = port_uuid
        if port_backend_id is not UNSET:
            field_dict["port_backend_id"] = port_backend_id
        if ip_on_router is not UNSET:
            field_dict["ip_on_router"] = ip_on_router
        if gateway_ip_on_router is not UNSET:
            field_dict["gateway_ip_on_router"] = gateway_ip_on_router
        if external_network_uuid is not UNSET:
            field_dict["external_network_uuid"] = external_network_uuid
        if external_network_name is not UNSET:
            field_dict["external_network_name"] = external_network_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        destination = d.pop("destination")

        def _parse_nexthop(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        nexthop = _parse_nexthop(d.pop("nexthop"))

        source = EffectiveRouteSourceEnum(d.pop("source"))

        def _parse_subnet_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subnet_uuid = _parse_subnet_uuid(d.pop("subnet_uuid", UNSET))

        subnet_name = d.pop("subnet_name", UNSET)

        subnet_cidr = d.pop("subnet_cidr", UNSET)

        def _parse_port_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        port_uuid = _parse_port_uuid(d.pop("port_uuid", UNSET))

        port_backend_id = d.pop("port_backend_id", UNSET)

        def _parse_ip_on_router(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ip_on_router = _parse_ip_on_router(d.pop("ip_on_router", UNSET))

        def _parse_gateway_ip_on_router(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gateway_ip_on_router = _parse_gateway_ip_on_router(d.pop("gateway_ip_on_router", UNSET))

        def _parse_external_network_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_network_uuid = _parse_external_network_uuid(d.pop("external_network_uuid", UNSET))

        external_network_name = d.pop("external_network_name", UNSET)

        effective_route = cls(
            destination=destination,
            nexthop=nexthop,
            source=source,
            subnet_uuid=subnet_uuid,
            subnet_name=subnet_name,
            subnet_cidr=subnet_cidr,
            port_uuid=port_uuid,
            port_backend_id=port_backend_id,
            ip_on_router=ip_on_router,
            gateway_ip_on_router=gateway_ip_on_router,
            external_network_uuid=external_network_uuid,
            external_network_name=external_network_name,
        )

        effective_route.additional_properties = d
        return effective_route

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
