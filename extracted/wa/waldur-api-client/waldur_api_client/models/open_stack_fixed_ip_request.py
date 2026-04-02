from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OpenStackFixedIpRequest")


@_attrs_define
class OpenStackFixedIpRequest:
    """
    Attributes:
        ip_address (str): IP address to assign to the port
        subnet_id (str): ID of the subnet in which to assign the IP address
    """

    ip_address: str
    subnet_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip_address: str
        ip_address = self.ip_address

        subnet_id = self.subnet_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ip_address": ip_address,
                "subnet_id": subnet_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_ip_address(data: object) -> str:
            return cast(str, data)

        ip_address = _parse_ip_address(d.pop("ip_address"))

        subnet_id = d.pop("subnet_id")

        open_stack_fixed_ip_request = cls(
            ip_address=ip_address,
            subnet_id=subnet_id,
        )

        open_stack_fixed_ip_request.additional_properties = d
        return open_stack_fixed_ip_request

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
