from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalSubnet")


@_attrs_define
class ExternalSubnet:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        backend_id (Union[Unset, str]):
        cidr (Union[Unset, str]):
        gateway_ip (Union[None, Unset, str]): An IPv4 or IPv6 address.
        ip_version (Union[Unset, int]):
        enable_dhcp (Union[Unset, bool]):
        allocation_pools (Union[Unset, Any]):
        dns_nameservers (Union[Unset, Any]):
        public_ip_range (Union[Unset, str]): Public CIDR mapped to this subnet (for carrier-grade NAT overlay)
        description (Union[Unset, str]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    cidr: Union[Unset, str] = UNSET
    gateway_ip: Union[None, Unset, str] = UNSET
    ip_version: Union[Unset, int] = UNSET
    enable_dhcp: Union[Unset, bool] = UNSET
    allocation_pools: Union[Unset, Any] = UNSET
    dns_nameservers: Union[Unset, Any] = UNSET
    public_ip_range: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        backend_id = self.backend_id

        cidr = self.cidr

        gateway_ip: Union[None, Unset, str]
        if isinstance(self.gateway_ip, Unset):
            gateway_ip = UNSET
        else:
            gateway_ip = self.gateway_ip

        ip_version = self.ip_version

        enable_dhcp = self.enable_dhcp

        allocation_pools = self.allocation_pools

        dns_nameservers = self.dns_nameservers

        public_ip_range = self.public_ip_range

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if cidr is not UNSET:
            field_dict["cidr"] = cidr
        if gateway_ip is not UNSET:
            field_dict["gateway_ip"] = gateway_ip
        if ip_version is not UNSET:
            field_dict["ip_version"] = ip_version
        if enable_dhcp is not UNSET:
            field_dict["enable_dhcp"] = enable_dhcp
        if allocation_pools is not UNSET:
            field_dict["allocation_pools"] = allocation_pools
        if dns_nameservers is not UNSET:
            field_dict["dns_nameservers"] = dns_nameservers
        if public_ip_range is not UNSET:
            field_dict["public_ip_range"] = public_ip_range
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        cidr = d.pop("cidr", UNSET)

        def _parse_gateway_ip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        gateway_ip = _parse_gateway_ip(d.pop("gateway_ip", UNSET))

        ip_version = d.pop("ip_version", UNSET)

        enable_dhcp = d.pop("enable_dhcp", UNSET)

        allocation_pools = d.pop("allocation_pools", UNSET)

        dns_nameservers = d.pop("dns_nameservers", UNSET)

        public_ip_range = d.pop("public_ip_range", UNSET)

        description = d.pop("description", UNSET)

        external_subnet = cls(
            uuid=uuid,
            name=name,
            backend_id=backend_id,
            cidr=cidr,
            gateway_ip=gateway_ip,
            ip_version=ip_version,
            enable_dhcp=enable_dhcp,
            allocation_pools=allocation_pools,
            dns_nameservers=dns_nameservers,
            public_ip_range=public_ip_range,
            description=description,
        )

        external_subnet.additional_properties = d
        return external_subnet

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
