from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetExternalGatewayFixedIPRequest")


@_attrs_define
class SetExternalGatewayFixedIPRequest:
    """
    Attributes:
        ip_address (str): IP address specification for the gateway port.
        subnet_id (Union[Unset, str]): Backend ID of the subnet.
    """

    ip_address: str
    subnet_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ip_address = self.ip_address

        subnet_id = self.subnet_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ip_address": ip_address,
            }
        )
        if subnet_id is not UNSET:
            field_dict["subnet_id"] = subnet_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ip_address = d.pop("ip_address")

        subnet_id = d.pop("subnet_id", UNSET)

        set_external_gateway_fixed_ip_request = cls(
            ip_address=ip_address,
            subnet_id=subnet_id,
        )

        set_external_gateway_fixed_ip_request.additional_properties = d
        return set_external_gateway_fixed_ip_request

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
