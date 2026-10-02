from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherNestedPublicIP")


@_attrs_define
class RancherNestedPublicIP:
    """
    Attributes:
        floating_ip (Union[Unset, str]):
        floating_ip_uuid (Union[Unset, UUID]):
        ip_address (Union[Unset, str]): An IPv4 or IPv6 address.
        external_ip_address (Union[Unset, str]): An IPv4 or IPv6 address.
    """

    floating_ip: Union[Unset, str] = UNSET
    floating_ip_uuid: Union[Unset, UUID] = UNSET
    ip_address: Union[Unset, str] = UNSET
    external_ip_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        floating_ip = self.floating_ip

        floating_ip_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.floating_ip_uuid, Unset):
            floating_ip_uuid = str(self.floating_ip_uuid)

        ip_address: Union[Unset, str]
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        external_ip_address: Union[Unset, str]
        if isinstance(self.external_ip_address, Unset):
            external_ip_address = UNSET
        else:
            external_ip_address = self.external_ip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if floating_ip is not UNSET:
            field_dict["floating_ip"] = floating_ip
        if floating_ip_uuid is not UNSET:
            field_dict["floating_ip_uuid"] = floating_ip_uuid
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if external_ip_address is not UNSET:
            field_dict["external_ip_address"] = external_ip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        floating_ip = d.pop("floating_ip", UNSET)

        _floating_ip_uuid = d.pop("floating_ip_uuid", UNSET)
        floating_ip_uuid: Union[Unset, UUID]
        if isinstance(_floating_ip_uuid, Unset):
            floating_ip_uuid = UNSET
        else:
            floating_ip_uuid = UUID(_floating_ip_uuid)

        def _parse_ip_address(data: object) -> Union[Unset, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, str], data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        def _parse_external_ip_address(data: object) -> Union[Unset, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, str], data)

        external_ip_address = _parse_external_ip_address(d.pop("external_ip_address", UNSET))

        rancher_nested_public_ip = cls(
            floating_ip=floating_ip,
            floating_ip_uuid=floating_ip_uuid,
            ip_address=ip_address,
            external_ip_address=external_ip_address,
        )

        rancher_nested_public_ip.additional_properties = d
        return rancher_nested_public_ip

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
