from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackCreateFloatingIPRequest")


@_attrs_define
class OpenStackCreateFloatingIPRequest:
    """
    Attributes:
        subnet (str):
        url (Union[Unset, str]):
        ip_address (Union[Unset, str]): Existing floating IP address in selected OpenStack tenant to be assigned to new
            virtual machine
    """

    subnet: str
    url: Union[Unset, str] = UNSET
    ip_address: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subnet = self.subnet

        url = self.url

        ip_address: Union[Unset, str]
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subnet": subnet,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        subnet = d.pop("subnet")

        url = d.pop("url", UNSET)

        def _parse_ip_address(data: object) -> Union[Unset, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, str], data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        open_stack_create_floating_ip_request = cls(
            subnet=subnet,
            url=url,
            ip_address=ip_address,
        )

        open_stack_create_floating_ip_request.additional_properties = d
        return open_stack_create_floating_ip_request

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
